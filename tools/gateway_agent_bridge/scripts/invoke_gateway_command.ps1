param(
  [string]$GatewayAction = "",
  [Parameter(Mandatory = $false)][string[]]$Arguments = @(),
  [switch]$AsJson
)

$gwinfoBat = 'C:\Program Files (x86)\BIOVIA\Materials Studio 24.1 x64 Server\etc\Gateway\gwinfo.bat'
if (!(Test-Path -LiteralPath $gwinfoBat)) {
  throw "gwinfo.bat not found: $gwinfoBat"
}

$stdoutPath = Join-Path $env:TEMP "gateway_agent_bridge.stdout.txt"
$stderrPath = Join-Path $env:TEMP "gateway_agent_bridge.stderr.txt"
if (Test-Path -LiteralPath $stdoutPath) { Remove-Item -LiteralPath $stdoutPath -Force -ErrorAction SilentlyContinue }
if (Test-Path -LiteralPath $stderrPath) { Remove-Item -LiteralPath $stderrPath -Force -ErrorAction SilentlyContinue }

$argumentList = @()
if ($GatewayAction -ne "") {
  $argumentList += $GatewayAction
}
$argumentList += $Arguments
if ($argumentList.Count -gt 0) {
  $proc = Start-Process `
    -FilePath $gwinfoBat `
    -ArgumentList $argumentList `
    -PassThru `
    -Wait `
    -NoNewWindow `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath
} else {
  $proc = Start-Process `
    -FilePath $gwinfoBat `
    -PassThru `
    -Wait `
    -NoNewWindow `
    -RedirectStandardOutput $stdoutPath `
    -RedirectStandardError $stderrPath
}

$stdout = if (Test-Path -LiteralPath $stdoutPath) {
  [string](Get-Content -LiteralPath $stdoutPath -Raw)
} else {
  ""
}

$stderr = if (Test-Path -LiteralPath $stderrPath) {
  [string](Get-Content -LiteralPath $stderrPath -Raw)
} else {
  ""
}

$result = [pscustomobject]@{
  ok = ($proc.ExitCode -eq 0)
  exitCode = $proc.ExitCode
  gatewayCommand = $gwinfoBat
  action = $GatewayAction
  args = $Arguments
  fullArgumentList = $argumentList
  stdout = $stdout
  stderr = $stderr
  stdoutPath = $stdoutPath
  stderrPath = $stderrPath
  nativeFailed = ($proc.ExitCode -ne 0) -or (-not [string]::IsNullOrWhiteSpace($stderr))
}

if ($AsJson) {
  $result | ConvertTo-Json -Depth 6
} else {
  $result
}
