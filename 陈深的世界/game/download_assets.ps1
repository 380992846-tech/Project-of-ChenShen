$ProgressPreference = 'SilentlyContinue'
$ErrorActionPreference = 'Continue'
$root = $PSScriptRoot  # game/
$assets = Join-Path $root 'assets'
New-Item -ItemType Directory -Force -Path $assets | Out-Null

# Collect every http(s) image URL referenced in the two source HTML files.
$sources = @(
    (Join-Path (Split-Path $root -Parent) '陈深的世界.html'),
    (Join-Path (Split-Path $root -Parent) '陈深的故事V5.html')
)
$urls = [System.Collections.Generic.List[string]]::new()
$seen = @{}
foreach ($s in $sources) {
    $c = Get-Content -Raw -Encoding UTF8 $s
    $m = [regex]::Matches($c, 'https?://[^\s''"`<>]+')
    foreach ($x in $m) {
        $u = $x.Value
        # trim trailing punctuation that could be part of code, not the URL
        $u = [regex]::Replace($u, '[\),;\]]+$', '')
        if ($u -notmatch '\.(jpg|jpeg|png|webp|gif)(\?|$)') { continue }
        if (-not $seen.ContainsKey($u)) { $seen[$u] = $true; $urls.Add($u) }
    }
}

$headers = @{ 'User-Agent' = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' }
$md5 = [System.Security.Cryptography.MD5]::Create()
$map = [ordered]@{}
$n = 0; $fail = 0; $skip = 0
foreach ($u in $urls) {
    $ext = 'jpg'
    if ($u -match '\.(jpg|jpeg|png|webp|gif)') { $ext = $matches[1]; if ($ext -eq 'jpeg') { $ext = 'jpg' } }
    $bytes = [System.Text.Encoding]::UTF8.GetBytes($u)
    $hash = [System.BitConverter]::ToString($md5.ComputeHash($bytes)).Replace('-', '').Substring(0, 10).ToLower()
    $rel = "assets/img_$hash.$ext"
    $out = Join-Path $root $rel
    $map[$u] = $rel
    if (Test-Path $out) { $skip++; continue }
    try {
        Invoke-WebRequest -Uri $u -OutFile $out -UseBasicParsing -TimeoutSec 90 -Headers $headers
        $n++
    } catch {
        $fail++
        Write-Output "FAIL $u :: $($_.Exception.Message)"
    }
}
$map | ConvertTo-Json | Set-Content -Encoding UTF8 (Join-Path $root 'url_map.json')
Write-Output "DONE unique=$($urls.Count) downloaded=$n skip=$skip fail=$fail"
