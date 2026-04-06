param(
    [Parameter(Mandatory = $true)]
    [string]$FilePath
)

$uri = "http://127.0.0.1:5000/predict"

if (-not (Test-Path $FilePath)) {
    Write-Host "❌ File not found: $FilePath"
    exit
}

Add-Type -AssemblyName System.Net.Http
$client = [System.Net.Http.HttpClient]::new()
$content = [System.Net.Http.MultipartFormDataContent]::new()

$fileStream = [System.IO.FileStream]::new($FilePath, [System.IO.FileMode]::Open)
$fileContent = [System.Net.Http.StreamContent]::new($fileStream)
$fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("image/jpeg")

$content.Add($fileContent, "file", [System.IO.Path]::GetFileName($FilePath))

$response = $client.PostAsync($uri, $content).Result
$result = $response.Content.ReadAsStringAsync().Result
Write-Output $result
