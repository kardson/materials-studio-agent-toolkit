param(
  [Parameter(Mandatory = $true)][string]$PerlScript,
  [Parameter(Mandatory = $false)][string[]]$Arguments = @(),
  [switch]$AsJson
)

$gwcmdBat = 'C:\Program Files (x86)\BIOVIA\Materials Studio 24.1 x64 Server\etc\Gateway\gwcmd.bat'
if (!(Test-Path -LiteralPath $gwcmdBat)) {
  throw "gwcmd.bat not found: $gwcmdBat"
}

if (!(Test-Path -LiteralPath $PerlScript)) {
  throw "Perl script not found: $PerlScript"
}

$stdoutPath = Join-Path $env:TEMP "gateway_runperl.stdout.txt"
$stderrPath = Join-Path $env:TEMP "gateway_runperl.stderr.txt"
if (Test-Path -LiteralPath $stdoutPath) { Remove-Item -LiteralPath $stdoutPath -Force -ErrorAction SilentlyContinue }
if (Test-Path -LiteralPath $stderrPath) { Remove-Item -LiteralPath $stderrPath -Force -ErrorAction SilentlyContinue }

$argumentList = @('/mode','runperl',$PerlScript) + $Arguments
$proc = Start-Process `
  -FilePath $gwcmdBat `
  -ArgumentList $argumentList `
  -PassThru `
  -Wait `
  -NoNewWindow `
  -RedirectStandardOutput $stdoutPath `
  -RedirectStandardError $stderrPath

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
  gatewayCommand = $gwcmdBat
  mode = 'runperl'
  perlScript = $PerlScript
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
