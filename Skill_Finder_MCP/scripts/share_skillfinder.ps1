param(
    [int]$Port = 8010,
    [string]$Token = $env:SKILLFINDER_AUTH_TOKEN
)

$ErrorActionPreference = "Stop"
$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

$lanIp = (Get-NetIPAddress -AddressFamily IPv4 -ErrorAction SilentlyContinue |
    Where-Object { $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.254.*' } |
    Select-Object -First 1 -ExpandProperty IPAddress)
if (-not $lanIp) { $lanIp = "127.0.0.1" }

$ruleName = "testskill-finder MCP ($Port)"
if (-not (Get-NetFirewallRule -DisplayName $ruleName -ErrorAction SilentlyContinue)) {
    try {
        New-NetFirewallRule -DisplayName $ruleName -Direction Inbound -Action Allow -Protocol TCP -LocalPort $Port | Out-Null
        Write-Host "Added inbound firewall rule '$ruleName'."
    }
    catch {
        Write-Warning "Could not add the firewall rule (run PowerShell as Administrator). Teammates may be blocked. Run:"
        Write-Host "  New-NetFirewallRule -DisplayName `"$ruleName`" -Direction Inbound -Action Allow -Protocol TCP -LocalPort $Port"
    }
}

$env:SKILLFINDER_AUTH_TOKEN = $Token
$serverUrl = "http://${lanIp}:$Port/mcp"

Write-Host ""
Write-Host "Sharing testskill-finder MCP at: $serverUrl"
if ($Token) {
    Write-Host "Bearer-token auth is ON. Teammates must send 'Authorization: Bearer <token>'."
}
else {
    Write-Host "No auth (trusted LAN only). Set `$env:SKILLFINDER_AUTH_TOKEN to require a token."
}
Write-Host "Teammates add this to their MCP client config (.mcp.json):"
Write-Host ""
Write-Host (@{ mcpServers = @{ "testskill-finder" = @{ type = "http"; url = $serverUrl } } } | ConvertTo-Json -Depth 5)
Write-Host ""
Write-Host "Press Ctrl+C to stop the server."
Write-Host ""

$uv = Get-Command uv -ErrorAction Stop
& $uv.Source run --directory $projectRoot skillfinder-mcp --transport http --host 0.0.0.0 --port $Port --path /mcp
