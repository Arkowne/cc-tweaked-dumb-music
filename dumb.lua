-- === CONFIGURATION PAR DÉFAUT ===
local dumbFile = "mid.dumb"

local firstRelayNumber = 109
local inst_side = "front"

local width = 36
local bytesPerLine = math.ceil(width / 8)
local delay = 0.125

-- === ARGUMENTS ===
local args = { ... }
if args[1] then
    dumbFile = args[1]
end
if args[2] then
    delay = tonumber(args[2]) or delay
end
local waitForRedstone = args[3] == "wait"

print("Lecture du fichier : " .. dumbFile)
print("Tempo (delay) : " .. delay .. " seconde(s)")

-- === ATTENDRE SIGNAL BOTTOM SI DEMANDÉ ===
if waitForRedstone then
    print("Attente d'un signal redstone (bottom)...")
    while not redstone.getInput("bottom") do
        sleep(0.1)
    end
end

-- === CHARGEMENT DU FICHIER BINAIRE ===
local file = fs.open(dumbFile, "rb")
if not file then
    error("Impossible d'ouvrir le fichier " .. dumbFile)
end

local dumb = {}
while true do
    local bytes = file.read(bytesPerLine)
    if not bytes then break end

    local row = {}
    for i = 1, width do
        local byteIndex = math.floor((i - 1) / 8) + 1
        local bitIndex = 7 - ((i - 1) % 8)
        local byte = bytes:byte(byteIndex)
        local bit = bit32.band(bit32.rshift(byte, bitIndex), 1)
        row[i] = bit == 1
    end
    table.insert(dumb, row)
end
file.close()
print("Chargement terminé. " .. #dumb .. " lignes détectées.")

-- === INITIALISATION DES RELAYS ===
local relays = {}
for i = 1, width do
    local relayName = "redstone_relay_" .. (firstRelayNumber + i - 1)
    relays[i] = peripheral.wrap(relayName)
    if not relays[i] then
        error("Impossible de trouver le périphérique : " .. relayName)
    end
end

-- === FONCTION POUR JOUER ET AFFICHER UNE LIGNE ===
local function playLine(row)
    local visual = ""
    for i = 1, width do
        relays[i].setOutput(inst_side, row[i])
        visual = visual .. (row[i] and "_" or "-")
    end
    print(visual)
end

-- === LECTURE UNIQUE ===
for y = 1, #dumb do
    playLine(dumb[y])
    sleep(delay)
end

-- === ÉTEINDRE TOUS LES RELAYS ===
for i = 1, width do
    relays[i].setOutput(inst_side, false)
end

print("Lecture terminée.")
