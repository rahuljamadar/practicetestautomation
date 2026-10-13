$ErrorActionPreference = "Stop"

$projectRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$serverUrl = "http://127.0.0.1:8000/mcp"
$inspectorUrl = "http://127.0.0.1:6274"

function Test-ListeningPort([int]$Port) {
    return $null -ne (Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1)
}

if (-not (Test-ListeningPort 8000)) {
    $uv = Get-Command uv -ErrorAction Stop
    Start-Process -FilePath $uv.Source `
        -ArgumentList @("run", "--directory", $projectRoot, "tc-mcp", "--transport", "http", "--host", "127.0.0.1", "--port", "8000", "--path", "/mcp") `
        -WorkingDirectory $projectRoot | Out-Null

    $serverReady = $false
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        $connection = [System.Net.Sockets.TcpClient]::new()
        try {
            $connectTask = $connection.ConnectAsync("127.0.0.1", 8000)
            if ($connectTask.Wait(1000) -and $connection.Connected) {
                $serverReady = $true
                break
            }
        }
        catch {
        }
        finally {
            $connection.Dispose()
        }
    }
    if (-not $serverReady) {
        throw "TestCreator MCP did not start on port 8000. Check that uv is installed and the port is free."
    }
}

$landingPage = & curl.exe --noproxy "*" -sS "http://127.0.0.1:8000/" 2>$null
$landingPageText = $landingPage -join "`n"
if ($LASTEXITCODE -ne 0 -or $landingPageText -notmatch "TestCreator MCP") {
    throw "Port 8000 is in use, but it is not serving the TestCreator MCP landing page."
}

Write-Host "TestCreator MCP endpoint: $serverUrl"
Write-Host "Browser help page: http://127.0.0.1:8000/"

if (-not (Test-ListeningPort 6274)) {
    $npx = Get-Command npx.cmd -ErrorAction Stop
    Write-Host "Starting Inspector in this terminal; keep it open while using the browser UI."
    & $npx.Source --yes "@modelcontextprotocol/inspector@2.10.1" --transport http --server-url $serverUrl
}
else {
    Write-Host "MCP Inspector is already running at $inspectorUrl; its current tokenized browser URL remains valid."
}
