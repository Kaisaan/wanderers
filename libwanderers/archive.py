"""
DATA.BIN archive unpacker.

The archive's directory listing lives inside SLPM_625.32: two parallel
tables (folder records at 0x0012D440, file records at 0x00129800) whose
pointers are relative to a base of 0xFFF80. File data sits in DATA.BIN
on 0x800-byte sector boundaries.
"""

import math
import os


BASE_PTR = 0xFFF80
READ_SIZE = 32
TERMINATOR = "\x00"
SECTOR = 0x800

FOLDER_TABLE_OFFSET = 0x0012D440
FILE_TABLE_OFFSET = 0x00129800
SLPM_NAME = "SLPM_625.32"


def unpack(data_file):
    slpm = open(os.path.join("extracted", "SLPM_625.32"), "rb")

    dataName = os.path.basename(data_file)

    dataFile = open(os.path.join("extracted", dataName), "rb")

    dataName = dataName.rstrip(".BIN")

    logFile = open(f"{dataName}.txt", "w", encoding="utf-8")

    os.makedirs(f"{dataName}", exist_ok=True)

    seekAddr = 0x0012D440

    foldersInfo = []

    while True:
        slpm.seek(seekAddr)

        folderPtr = int.from_bytes(slpm.read(4), "little")
        folderIndex = int.from_bytes(slpm.read(4), "little")
        filecount = int.from_bytes(slpm.read(4), "little")

        if (folderPtr <= 0):
            break

        folderPtr = folderPtr - BASE_PTR
        print(f"{folderPtr}\t{folderIndex}\t{filecount}\t{slpm.tell():X}")

        slpm.seek(folderPtr)
        folderName = slpm.read(READ_SIZE).decode(
            encoding="shift-jis", errors="backslashreplace"
        )
        folderName = folderName[: folderName.find(TERMINATOR)]

        seekAddr = seekAddr + 12

        foldersInfo.append([folderName, folderPtr, folderIndex, filecount])

    seekAddr = 0x00129800

    slpm.seek(seekAddr)

    for i in range(len(foldersInfo)):
        logFile.write(
            f"{foldersInfo[i][0]} {foldersInfo[i][1]} {foldersInfo[i][2]} {foldersInfo[i][3]}\n"
        )

        for j in range(foldersInfo[i][3]):
            slpm.seek(seekAddr)
            filePtr = int.from_bytes(slpm.read(4), "little")
            fileSize = int.from_bytes(slpm.read(4), "little")
            fileStart = int.from_bytes(slpm.read(4), "little")
            fileEnd = int.from_bytes(slpm.read(4), "little")

            filePtr = filePtr - BASE_PTR

            slpm.seek(filePtr)
            fileName = slpm.read(READ_SIZE).decode(
                encoding="shift-jis", errors="backslashreplace"
            )
            fileName = fileName[: fileName.find(TERMINATOR)]

            fileName = fileName.replace(" ", "_")

            os.makedirs(f"{dataName}{foldersInfo[i][0]}", exist_ok=True)
            file = open(f"{dataName}{foldersInfo[i][0]}{fileName}", "wb")

            dataFile.seek(fileStart * SECTOR)
            fileData = dataFile.read(fileSize)

            file.write(fileData)

            logFile.write(f"{fileName} {filePtr} {fileSize} {fileStart} {fileEnd}\n")

            seekAddr = seekAddr + 16


def pack(data_file):
    slpm = open(os.path.join("translated", SLPM_NAME), "r+b")

    dataName = os.path.basename(data_file)
    dataFile = open(os.path.join("translated", dataName), "wb")
    dataName = dataName.rstrip(".BIN")
    logFile = open(f"{dataName}.txt", "r", encoding="utf-8")

    slpm.seek(FILE_TABLE_OFFSET)
    startSector = 0

    while True:
        line = logFile.readline()
        if line == "":
            break
        folderInfo = line.strip("\n").split()
        folderName = folderInfo[0]
        folderAmount = int(folderInfo[3])

        for _ in range(folderAmount):
            line = logFile.readline()
            fileInfo = line.strip("\n").split()
            fileName = fileInfo[0]
            filePtr = int(fileInfo[1])

            filePath = f"{dataName}{folderName}{fileName}"
            with open(filePath, "rb") as f:
                fileData = f.read()

            fileSize = len(fileData)
            sectorSize = math.ceil(fileSize / SECTOR)
            padding = bytes((sectorSize * SECTOR) - fileSize)

            dataFile.write(fileData)
            dataFile.write(padding)

            slpm.write((filePtr + BASE_PTR).to_bytes(4, "little"))
            slpm.write(fileSize.to_bytes(4, "little"))
            slpm.write(startSector.to_bytes(4, "little"))
            slpm.write(sectorSize.to_bytes(4, "little"))

            startSector += sectorSize

    slpm.close()
    dataFile.close()
    logFile.close()
