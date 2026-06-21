param(
  [Parameter(Mandatory = $true)][string]$RunMatScriptBat,
  [Parameter(Mandatory = $true)][string]$ScriptPath,
  [int]$TimeoutSeconds = 1800,
  [switch]$ProjectMode,
  [int]$Cores = 0,
  [string[]]$ScriptArguments = @(),
  [switch]$AsJson
)

if (!(Test-Path -LiteralPath $RunMatScriptBat)) {
  throw "RunMatScript.bat not found: $RunMatScriptBat"
}

if (!(Test-Path -LiteralPath $ScriptPath)) {
  throw "MaterialsScript file not found: $ScriptPath"
}

$scriptDir = Split-Path -Parent $ScriptPath
$scriptBase = [System.IO.Path]::GetFileNameWithoutExtension($ScriptPath)
$nativeStdoutPath = Join-Path $scriptDir "$([System.IO.Path]::GetFileName($ScriptPath)).out"
$nativeLogPath = Join-Path $scriptDir "${scriptBase}MatStudioLog.htm"

$arguments = @()
if ($Cores -gt 0) {
  $arguments += "-np"
  $arguments += "$Cores"
}
if ($ProjectMode) {
  $arguments += "-project"
}
$arguments += $scriptBase
if ($ScriptArguments.Count -gt 0) {
  $arguments += "--"
  foreach ($arg in $ScriptArguments) {
    if ($arg -match '\s') {
      $arguments += "`"$arg`""
    } else {
      $arguments += $arg
    }
  }
}

$process = Start-Process `
  -FilePath $RunMatScriptBat `
  -ArgumentList $arguments `
  -WorkingDirectory $scriptDir `
  -PassThru `
  -WindowStyle Hidden

$timedOut = $false
$null = Wait-Process -Id $process.Id -Timeout $TimeoutSeconds -ErrorAction SilentlyContinue
if (-not $process.HasExited) {
  $timedOut = $true
  try {
    Stop-Process -Id $process.Id -Force -ErrorAction Stop
  } catch {
  }
}
$process.Refresh()

$nativeStdout = if (Test-Path -LiteralPath $nativeStdoutPath) {
  [string](Get-Content -LiteralPath $nativeStdoutPath -Raw)
} else {
  ""
}

$nativeLog = if (Test-Path -LiteralPath $nativeLogPath) {
  [string](Get-Content -LiteralPath $nativeLogPath -Raw)
} else {
  ""
}

$nativeFailed = ($nativeStdout -match 'Completion status:\s*\(FAIL\)') -or ($nativeLog -match 'Completion status:\s*\(FAIL\)') -or ($nativeLog -match 'ERROR')

$result = [pscustomobject]@{
  ok = (!$timedOut -and $process.ExitCode -eq 0 -and -not $nativeFailed)
  exitCode = $process.ExitCode
  timedOut = $timedOut
  runMatScriptBat = $RunMatScriptBat
  scriptPath = $ScriptPath
  projectMode = [bool]$ProjectMode
  cores = $Cores
  scriptArguments = $ScriptArguments
  timeoutSeconds = $TimeoutSeconds
  nativeStdoutPath = $nativeStdoutPath
  nativeLogPath = $nativeLogPath
  nativeStdout = $nativeStdout
  nativeLog = $nativeLog
  nativeFailed = $nativeFailed
}

if ($AsJson) {
  $result | ConvertTo-Json -Depth 6
} else {
  $result
}
