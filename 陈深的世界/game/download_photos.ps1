$ProgressPreference = 'SilentlyContinue'
$repo = '380992846-tech/Project-of-ChenShen'
$dir  = Join-Path $PSScriptRoot 'photos'
New-Item -ItemType Directory -Force -Path $dir | Out-Null

$headers = @{ 'User-Agent' = 'Mozilla/5.0' }
$apiUrl  = "https://api.github.com/repos/$repo/contents/photos"
$items   = Invoke-RestMethod -Uri $apiUrl -Headers $headers -TimeoutSec 60

$n = 0
$failed = @()
foreach ($it in $items) {
    $name = $it.name
    $out  = Join-Path $dir $name
    if (Test-Path $out) { continue }
    $raw = "https://raw.githubusercontent.com/$repo/main/photos/$([uri]::EscapeDataString($name))"
    try {
        Invoke-WebRequest -Uri $raw -OutFile $out -UseBasicParsing -TimeoutSec 120 -Headers $headers
        $n++
        Write-Output "OK   $name"
    } catch {
        $failed += $name
        Write-Output "FAIL $name :: $($_.Exception.Message)"
    }
}
Write-Output "DONE downloaded_new=$n total=$(Get-ChildItem $dir -File).Count failed=$($failed.Count)"
