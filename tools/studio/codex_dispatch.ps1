<# Explicit operator-run dispatch. DryRun never starts a model. #>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][ValidatePattern('^[A-Za-z0-9_-]+$')][string]$Task,
    [string]$ProjectRoot = (Join-Path $PSScriptRoot '..\..'),
    [string]$CodexCommand = 'codex',
    [switch]$DryRun
)
$ErrorActionPreference = 'Stop'
$project = (Resolve-Path -LiteralPath $ProjectRoot).Path
foreach ($rel in @('AGENTS.md', 'production\OPUS_TO_CODEX.md')) {
    if (-not (Test-Path -LiteralPath (Join-Path $project $rel) -PathType Leaf)) {
        throw "Missing required project file: $rel"
    }
}
$prompt = "Read AGENTS.md and production/OPUS_TO_CODEX.md. Complete only task $Task. " +
    'Use the assigned file scope and the current user instructions. ' +
    'Report result, changed files, evidence and open decisions at the top of production/CODEX_TO_OPUS.md.'
if ($DryRun) {
    [pscustomobject]@{ task = $Task; project = $project; command = $CodexCommand; prompt = $prompt; launches_model = $false } | ConvertTo-Json
    exit 0
}
$command = Get-Command $CodexCommand -ErrorAction Stop
$runs = Join-Path $project 'production\codex_runs'
New-Item -ItemType Directory -Path $runs -Force | Out-Null
$stamp = Get-Date -Format 'yyyyMMdd_HHmmss_fff'
$log = Join-Path $runs ($Task + '_' + $stamp + '.log')
$last = Join-Path $runs ($Task + '_' + $stamp + '.last.md')
& $command.Source exec -C $project --sandbox workspace-write -o $last $prompt *> $log
$result = $LASTEXITCODE
Write-Output "Task $Task exited $result. Log: $log. Report: $last"
exit $result
