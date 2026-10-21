# Read-only installation probe. Does not launch games or read their content.
[CmdletBinding()]
param(
    [string]$ZZZRoot = 'E:\SteamLibrary\steamapps\common\Zenless Zone Zero',
    [string]$FortniteRoot = 'E:\jogos\Fortnite'
)
$ErrorActionPreference = 'Stop'
$targets = @(
    @{id='host'; root=$ZZZRoot; exe='games\ZenlessZoneZero Game\ZenlessZoneZero.exe'},
    @{id='companion'; root=$FortniteRoot; exe='FortniteGame\Binaries\Win64\FortniteClient-Win64-Shipping.exe'}
)
$rows = foreach ($target in $targets) {
    $exe = Join-Path $target.root $target.exe
    $present = Test-Path -LiteralPath $exe -PathType Leaf
    $version = if ($present) { (Get-Item -LiteralPath $exe).VersionInfo.FileVersion } else { $null }
    [pscustomobject]@{
        id=$target.id
        directoryExists=(Test-Path -LiteralPath $target.root -PathType Container)
        executableExists=$present
        fileVersion=$version
        runtimeIntegrationVerified=$false
    }
}
ConvertTo-Json -InputObject @($rows) -Depth 3
if (@($rows | Where-Object { -not $_.executableExists }).Count -gt 0) { exit 1 }
