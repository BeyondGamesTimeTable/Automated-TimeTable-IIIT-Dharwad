# Update back button styling in all timetable HTML files

$htmlFiles = Get-ChildItem -Path "timetable_html" -Filter "*Timetable.html"

$oldButtonStyle = @'
        .back-button {
            display: inline-block;
            margin: 20px;
            padding: 12px 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 25px;
            font-weight: bold;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        
        .back-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
'@

$newButtonStyle = @'
        .back-button {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin: 20px;
            padding: 14px 32px;
            background: linear-gradient(135deg, #56ab2f 0%, #a8e063 100%);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1.05em;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: 0 6px 20px rgba(86, 171, 47, 0.35);
            position: relative;
            overflow: hidden;
            border: 2px solid rgba(255, 255, 255, 0.2);
        }
        
        .back-button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }
        
        .back-button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 10px 30px rgba(86, 171, 47, 0.5);
            border-color: rgba(255, 255, 255, 0.4);
        }
        
        .back-button:hover::before {
            width: 300px;
            height: 300px;
        }
        
        .back-button:active {
            transform: translateY(-1px) scale(0.98);
            box-shadow: 0 4px 15px rgba(86, 171, 47, 0.4);
        }
'@

foreach ($file in $htmlFiles) {
    Write-Host "Updating $($file.Name)..."
    $content = Get-Content $file.FullName -Raw
    $content = $content -replace [regex]::Escape($oldButtonStyle), $newButtonStyle
    Set-Content $file.FullName -Value $content
}

Write-Host "✅ All files updated successfully!"
