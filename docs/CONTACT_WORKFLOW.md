# HAL Guardian — Contact Memory Workflow
## For: Saturday Meet-and-Greet at Gemma Hackathon 2026

**Date:** 2026-07-25 | **Event:** GDG Windsor Build with AI — Gemma Hackathon
**Prepared by:** HAL on 2026-07-21

---

## Overview

This workflow captures people Steve meets at the hackathon, tracks follow-ups, and manages consent — so HAL can help Steve nurture relationships without being creepy.

**Three methods:**
1. **Digital** — PowerShell script on Steve's laptop → inserts into `agent_memory` MySQL
2. **Mobile** — Simple HTML form running on localhost MAMP → works from phone
3. **Paper backup** — Printable markdown form (in case tech fails)

---

## Database Schema

**Database:** `agent_memory` (local MAMP MySQL)
**Table:** `_HAL-event_contacts`

```sql
CREATE TABLE IF NOT EXISTS `_HAL-event_contacts` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    instance_id VARCHAR(36) DEFAULT NULL,
    event_name VARCHAR(100) NOT NULL DEFAULT 'Gemma Hackathon 2026',
    event_date DATE NOT NULL DEFAULT '2026-07-25',
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) DEFAULT NULL,
    company VARCHAR(100) DEFAULT NULL,
    role VARCHAR(100) DEFAULT NULL,
    what_caught_ear TEXT DEFAULT NULL,
    notes TEXT DEFAULT NULL,
    follow_up_date DATE DEFAULT NULL,
    follow_up_done TINYINT(1) DEFAULT 0,
    consent_granted TINYINT(1) DEFAULT 0,
    consent_method VARCHAR(50) DEFAULT NULL,
    consent_date TIMESTAMP NULL DEFAULT NULL,
    tags VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_event_date (event_date),
    INDEX idx_follow_up (follow_up_date, follow_up_done),
    INDEX idx_consent (consent_granted),
    INDEX idx_tags (tags)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

**Why these fields:**
| Field | Purpose |
|-------|---------|
| `instance_id` | HAL parallel session isolation |
| `event_name` | Reusable for future events |
| `what_caught_ear` | Their stated interest — crucial for personalized follow-up |
| `consent_granted` + `consent_method` + `consent_date` | GDPR-lite compliance |
| `follow_up_date` + `follow_up_done` | Task management for Steve |
| `tags` | Quick categorization: `investor`, `developer`, `judge`, `media`, `potential_client` |

---

## PowerShell Scripts

### 1. `Add-EventContact.ps1` — Quick capture at the event

```powershell
# Add-EventContact.ps1
# Quick contact capture for Steve at events
# Usage: .\Add-EventContact.ps1 -Name "Jane Doe" -Email "jane@example.com" -WhatCaughtEar "The audit engine"

param(
    [Parameter(Mandatory=$true)]
    [string]$Name,
    
    [string]$Email = $null,
    [string]$Company = $null,
    [string]$Role = $null,
    [string]$WhatCaughtEar = $null,
    [string]$Notes = $null,
    [string]$Tags = $null,
    [string]$EventName = "Gemma Hackathon 2026",
    [string]$EventDate = "2026-07-25"
)

$mysqlBin = "C:\MAMP\bin\mysql\bin\mysql.exe"
$defaultsFile = "C:\Users\Steve Vogelaar\.my.cnf"

# Interactive consent capture
$consent = Read-Host "Did they give consent to follow up? (y/n)"
$consentGranted = if ($consent -eq 'y') { 1 } else { 0 }
$consentMethod = if ($consentGranted) { Read-Host "How? (verbal/email/business_card/other)" } else { $null }

# Build SQL
$sql = @"
INSERT INTO \`_HAL-event_contacts\`
(name, email, company, role, what_caught_ear, notes, event_name, event_date, consent_granted, consent_method, consent_date, tags)
VALUES
('$($Name -replace "'", "''")',
 '$($Email -replace "'", "''")',
 '$($Company -replace "'", "''")',
 '$($Role -replace "'", "''")',
 '$($WhatCaughtEar -replace "'", "''")',
 '$($Notes -replace "'", "''")',
 '$($EventName -replace "'", "''")',
 '$EventDate',
 $consentGranted,
 '$($consentMethod -replace "'", "''")',
 $(if ($consentGranted) { "NOW()" } else { "NULL" }),
 '$($Tags -replace "'", "''")');
"@

# Execute
$sql | & $mysqlBin --defaults-file="$defaultsFile" -D agent_memory

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Contact saved: $Name" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to save contact" -ForegroundColor Red
}
```

### 2. `Get-EventContacts.ps1` — Review who you met

```powershell
# Get-EventContacts.ps1
# List contacts from an event
# Usage: .\Get-EventContacts.ps1 -EventDate "2026-07-25"

param(
    [string]$EventDate = "2026-07-25",
    [string]$Tag = $null,
    [switch]$PendingFollowUp
)

$mysqlBin = "C:\MAMP\bin\mysql\bin\mysql.exe"
$defaultsFile = "C:\Users\Steve Vogelaar\.my.cnf"

$where = "event_date = '$EventDate'"
if ($Tag) { $where += " AND tags LIKE '%$Tag%'" }
if ($PendingFollowUp) { $where += " AND follow_up_done = 0 AND follow_up_date IS NOT NULL" }

$sql = @"
SELECT id, name, email, company, role, what_caught_ear, 
       consent_granted, follow_up_date, follow_up_done, tags
FROM \`_HAL-event_contacts\`
WHERE $where
ORDER BY created_at DESC;
"@

& $mysqlBin --defaults-file="$defaultsFile" -D agent_memory -e "$sql"
```

### 3. `Set-FollowUpDone.ps1` — Mark follow-up complete

```powershell
# Set-FollowUpDone.ps1
# Mark a follow-up as done
# Usage: .\Set-FollowUpDone.ps1 -Id 5

param(
    [Parameter(Mandatory=$true)]
    [int]$Id
)

$mysqlBin = "C:\MAMP\bin\mysql\bin\mysql.exe"
$defaultsFile = "C:\Users\Steve Vogelaar\.my.cnf"

$sql = "UPDATE \`_HAL-event_contacts\` SET follow_up_done = 1 WHERE id = $Id;"
& $mysqlBin --defaults-file="$defaultsFile" -D agent_memory -e "$sql"

Write-Host "Follow-up marked complete for contact ID $Id" -ForegroundColor Green
```

---

## Mobile HTML Form (Phone-Friendly)

Save as `mobile-contact-form.html` in `_HAL\mobile\`:

```html
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>HAL Contact Capture</title>
    <style>
        body { font-family: system-ui; max-width: 400px; margin: 20px auto; padding: 10px; }
        input, textarea, select { width: 100%; margin: 5px 0 15px 0; padding: 10px; font-size: 16px; }
        button { width: 100%; padding: 15px; font-size: 18px; background: #0066cc; color: white; border: none; }
        .success { color: green; }
        .error { color: red; }
    </style>
</head>
<body>
    <h2>🤝 New Contact</h2>
    <form id="contactForm">
        <input type="text" id="name" placeholder="Name *" required>
        <input type="email" id="email" placeholder="Email">
        <input type="text" id="company" placeholder="Company">
        <input type="text" id="role" placeholder="Role (e.g., Developer, Judge)">
        <input type="text" id="what_caught_ear" placeholder="What caught their interest?">
        <textarea id="notes" placeholder="Quick notes"></textarea>
        <select id="consent">
            <option value="0">No follow-up consent</option>
            <option value="1">Consent given ✓</option>
        </select>
        <input type="text" id="tags" placeholder="Tags: investor, developer, judge, media">
        <button type="submit">Save Contact</button>
    </form>
    <div id="result"></div>

    <script>
        document.getElementById('contactForm').onsubmit = async (e) => {
            e.preventDefault();
            const data = {
                name: document.getElementById('name').value,
                email: document.getElementById('email').value,
                company: document.getElementById('company').value,
                role: document.getElementById('role').value,
                what_caught_ear: document.getElementById('what_caught_ear').value,
                notes: document.getElementById('notes').value,
                consent: document.getElementById('consent').value,
                tags: document.getElementById('tags').value
            };
            
            // POST to a local PHP endpoint (see below)
            try {
                const res = await fetch('http://localhost:8888/save-contact.php', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(data)
                });
                const result = await res.json();
                document.getElementById('result').innerHTML = 
                    result.ok ? '<p class="success">✅ Saved!</p>' : '<p class="error">❌ Error</p>';
                if (result.ok) document.getElementById('contactForm').reset();
            } catch (err) {
                document.getElementById('result').innerHTML = '<p class="error">❌ ' + err.message + '</p>';
            }
        };
    </script>
</body>
</html>
```

**Backend PHP (`save-contact.php`):**
```php
<?php
header('Content-Type: application/json');
$config = parse_ini_file('C:/Users/Steve Vogelaar/.my.cnf');
$dsn = "mysql:host=127.0.0.1;dbname=agent_memory;charset=utf8mb4";
$pdo = new PDO($dsn, $config['user'] ?? 'root', $config['password'] ?? 'root');

$data = json_decode(file_get_contents('php://input'), true);
$stmt = $pdo->prepare("
    INSERT INTO `_HAL-event_contacts`
    (name, email, company, role, what_caught_ear, notes, event_name, event_date, consent_granted, tags)
    VALUES (?, ?, ?, ?, ?, ?, 'Gemma Hackathon 2026', '2026-07-25', ?, ?)
");

$ok = $stmt->execute([
    $data['name'], $data['email'], $data['company'], $data['role'],
    $data['what_caught_ear'], $data['notes'], $data['consent'], $data['tags']
]);

echo json_encode(['ok' => $ok, 'id' => $pdo->lastInsertId()]);
```

---

## Paper Backup Form (Printable)

Print this page and bring 20 copies. If your laptop dies, you still capture data.

```
═══════════════════════════════════════════════════════════════
  HAL GUARDIAN — CONTACT CAPTURE
  Gemma Hackathon 2026 — July 25, 2026
═══════════════════════════════════════════════════════════════

Name: _________________________________________

Email: ________________________________________

Company / Role: ________________________________

What caught their interest?
_________________________________
_________________________________

Quick notes:
_________________________________
_________________________________
_________________________________

☐ Consent to follow up given
   Method: ☐ Verbal  ☐ Business card  ☐ Email reply

Tags: ☐ Investor  ☐ Developer  ☐ Judge  ☐ Media  ☐ Potential Client
      ☐ Partner   ☐ Mentor     ☐ Other: ________________

Follow-up by: ________ / ________ / ________ (date)

═══════════════════════════════════════════════════════════════
```

---

## Saturday Workflow

### Morning (Before Event)
1. Run the schema setup (once):
   ```powershell
   mysql --defaults-file="C:\Users\Steve Vogelaar\.my.cnf" -D agent_memory < contact-schema.sql
   ```
2. Test the PowerShell script with a fake entry
3. Open the mobile form in your phone browser
4. Print 20 paper backup forms
5. Pack a pen

### During Event
| Situation | Method |
|---|---|
| At booth, laptop open | PowerShell script (`Add-EventContact.ps1`) |
| Walking around, no laptop | Mobile form on phone (localhost:8888) |
| Phone dead / no signal | Paper form → type into PowerShell later |
| Someone hands you a card | Paper form → photo of card attached to notes |

### Evening (After Event)
1. If any paper forms, batch-enter via PowerShell
2. Run `Get-EventContacts.ps1 -PendingFollowUp` to see who needs action
3. HAL will email you the list Sunday morning

---

## Post-Event Follow-Up Template

**For contacts with `consent_granted = 1`:**

```
Subject: Great meeting you at the Gemma Hackathon!

Hi [Name],

It was great meeting you at the GDG Windsor hackathon on Saturday.
You mentioned [what_caught_ear] — I'd love to keep the conversation going.

[Specific ask based on tag:]
- Investor: We're not raising yet, but I'd love to send you our 90-day validation plan.
- Developer: The repo is public — try `ollama pull gemma4:e2b` and let me know what breaks.
- Judge: Thank you for your time and feedback. Your [specific feedback] shaped our final pitch.
- Media: Happy to do a demo or interview anytime. Here's the repo and the video.
- Potential Client: Let's schedule a 15-minute discovery call. What's your week look like?

HAL — my AI collaborator — and I are building privacy-first AI tools.
If you know anyone who needs local security review, send them our way.

Best,
Steve Vogelaar
hal@itoversight.ca
https://github.com/stevevogelaar/HAL-Guardian
```

---

## Quick Commands Reference

```powershell
# Add a contact (interactive)
Add-EventContact.ps1 -Name "Jane Doe" -Email "jane@example.com" -WhatCaughtEar "The audit engine" -Tags "developer,potential_client"

# List all contacts from Saturday
Get-EventContacts.ps1 -EventDate "2026-07-25"

# List only investors and media
Get-EventContacts.ps1 -EventDate "2026-07-25" -Tag "investor"
Get-EventContacts.ps1 -EventDate "2026-07-25" -Tag "media"

# Who needs follow-up?
Get-EventContacts.ps1 -EventDate "2026-07-25" -PendingFollowUp

# Mark follow-up done
Set-FollowUpDone.ps1 -Id 5
```

---

## Privacy & Consent Rules

1. **Always ask** before adding someone to any follow-up list
2. **Log the method** — verbal, card exchange, email reply
3. **No cold outreach** to anyone with `consent_granted = 0`
4. **Tag accurately** — `investor` vs `potential_client` changes the follow-up tone
5. **Delete on request** — if someone says "take me off your list," mark `consent_granted = 0` and note the date

---

*Generated by HAL on 2026-07-21. Version 1.0. Test before Saturday.*
