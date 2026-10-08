<#
  codex_dispatch.ps1 - Opus dispatches work to Codex directly (no owner relay needed).
  (ASCII only on purpose: Windows PowerShell 5.1 misreads UTF-8 without BOM.)

  Usage:
    powershell -File tools/studio/codex_dispatch.ps1 -Task C-01
      -> Codex reads AGENTS.md + production/OPUS_TO_CODEX.md and does task C-01.
    powershell -File tools/studio/codex_dispatch.ps1 -Task X -PromptFile production/codex_runs/X.prompt.md
      -> Codex follows the (UTF-8, Chinese ok) instructions in that file.

  Output:
    production/codex_runs/<Task>_<stamp>.log      full transcript
    production/codex_runs/<Task>_<stamp>.last.md  Codex's final report
  Auth: uses the ChatGPT login of the local Codex desktop app (~/.codex). No credentials handled here.
#>
param(
  [Parameter(Mandatory = $true)][string]$Task,
  [string]$PromptFile = ""
)
$game = "E:\Lv\game"
$codex = "E:\Lv\studio-tools\codex-cli\node_modules\.bin\codex.cmd"
$runs = Join-Path $game "production\codex_runs"
New-Item -ItemType Directory -Force $runs | Out-Null
$stamp = Get-Date -Format "yyyyMMdd_HHmm"
$log = Join-Path $runs ($Task + "_" + $stamp + ".log")
$last = Join-Path $runs ($Task + "_" + $stamp + ".last.md")

if ($PromptFile) {
  $prompt = "You are Codex, the execution team of this project (Claude Opus is the director). " +
            "Read AGENTS.md first. Then read the file '" + $PromptFile + "' (UTF-8, Chinese) and do exactly what it says. " +
            "Only edit files it assigns to you. Write your report at the TOP of production/CODEX_TO_OPUS.md in Chinese."
} else {
  $prompt = "You are Codex, the execution team of this project (Claude Opus is the director). " +
            "Read AGENTS.md, then production/OPUS_TO_CODEX.md, and do ONLY task " + $Task + ". " +
            "Only edit files that task assigns to you; Opus is editing js/, css/, index.html, assets/manifest.js and tools/art/ at the same time - do not touch them. " +
            "When done, write your report at the TOP of production/CODEX_TO_OPUS.md in Chinese (result / files changed / evidence / decisions needed). " +
            "Stop and report if a step needs login, payment, admin rights or security changes."
}

# Playwright browsers live inside the workspace (the sandbox can only write there)
$env:PLAYWRIGHT_BROWSERS_PATH = Join-Path $game "tools\qa\.browsers"

("[" + (Get-Date -Format s) + "] dispatch " + $Task) | Out-File -FilePath $log -Encoding utf8
& $codex exec -C $game --approve-for-me `
  -c "sandbox_workspace_write.network_access=true" `
  --add-dir "E:\Lv\studio-tools\mingit" `
  -o $last $prompt *>> $log
("[" + (Get-Date -Format s) + "] exit " + $LASTEXITCODE) | Out-File -FilePath $log -Encoding utf8 -Append
Write-Output ("done " + $Task + " -> " + $last)
