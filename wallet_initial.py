#!/usr/bin/env python3
"""
🔐 5470 WALLET INICIAL - VERSIÓN LIMPIA 🔐
Wallet inicial con funcionalidades básicas y actualizaciones en tiempo real
"""

import webbrowser
import time
import threading
import sys
from datetime import datetime
import uuid
import json
import hashlib
import random

def print_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                    🔐 5470 WALLET INICIAL 🔐                ║
    ║                                                              ║
    ║  🚀 Blockchain Wallet Technology                             ║
    ║  ⛏️  Mining & Transactions                                  ║
    ║  🔄 Auto-Update Data                                        ║
    ║  🌐 Real-time Synchronization                               ║
    ║                                                              ║
    ║  📍 URL: http://localhost:8002                               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def open_browser():
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:8002")
        print("🌐 ¡Navegador abierto! Tu 5470 Wallet está lista!")
    except:
        print("🌐 Abre manualmente: http://localhost:8002")

# Wallet State - Datos actualizables
wallet_data = {
    "address": "5470_" + hashlib.sha256(str(random.random()).encode()).hexdigest()[:16],
    "balance": 500.0,
    "transactions": [],
    "is_mining": False,
    "mining_rewards": 0,
    "vpn_connected": False,
    "last_update": datetime.now().isoformat()
}

def main():
    print_banner()
    
    print("🚀 Iniciando 5470 Wallet Inicial...")
    print("🔄 Configurando auto-actualización de datos...")
    
    # Abrir navegador en segundo plano
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        from fastapi import FastAPI, Request
        from fastapi.responses import HTMLResponse
        import uvicorn
        
        app = FastAPI(title="5470 Wallet Inicial")
        
        # HTML Template con auto-actualización
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>5470 Wallet Inicial</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Arial', sans-serif;
                    background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
                    min-height: 100vh; color: white; padding: 20px;
                }
                .container { max-width: 600px; margin: 0 auto; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { font-size: 2.2em; margin-bottom: 10px; }
                .wallet-box { 
                    background: rgba(255,255,255,0.15); 
                    backdrop-filter: blur(10px);
                    border-radius: 15px; padding: 25px; margin-bottom: 20px;
                    border: 1px solid rgba(255,255,255,0.3);
                }
                .balance-display { 
                    font-size: 2.5em; text-align: center; margin-bottom: 15px;
                    color: #FFD700; font-weight: bold;
                }
                .address-display { 
                    font-size: 0.85em; text-align: center; margin-bottom: 25px;
                    opacity: 0.9; word-break: break-all;
                }
                .button-grid { 
                    display: grid; grid-template-columns: 1fr 1fr; gap: 15px; 
                    margin-bottom: 20px;
                }
                .btn { 
                    padding: 15px; border: none; border-radius: 8px; font-size: 16px;
                    cursor: pointer; transition: all 0.3s; font-weight: bold;
                    color: white;
                }
                .btn-send { background: #e74c3c; }
                .btn-receive { background: #27ae60; }
                .btn-mine { background: #f39c12; }
                .btn-vpn { background: #8e44ad; }
                .btn:hover { transform: translateY(-2px); opacity: 0.9; }
                .status-panel { 
                    background: rgba(0,0,0,0.3); padding: 15px; border-radius: 8px;
                    display: flex; justify-content: space-between; margin-bottom: 20px;
                }
                .transactions-panel { 
                    background: rgba(0,0,0,0.2); padding: 15px; border-radius: 8px;
                    max-height: 200px; overflow-y: auto;
                }
                .tx-item { 
                    padding: 8px; margin-bottom: 8px; background: rgba(255,255,255,0.1);
                    border-radius: 5px; font-size: 14px;
                }
                .update-indicator { 
                    position: fixed; top: 10px; right: 10px; 
                    background: #27ae60; padding: 5px 10px; border-radius: 15px;
                    font-size: 12px; opacity: 0.8;
                }
                .notification { 
                    position: fixed; top: 50px; right: 10px; 
                    background: #f39c12; padding: 10px 15px; border-radius: 8px;
                    font-size: 14px; z-index: 1000; animation: slideIn 0.5s;
                }
                @keyframes slideIn { from { transform: translateX(100%); } to { transform: translateX(0); } }
            </style>
        </head>
        <body>
            <div class="update-indicator" id="updateIndicator">🔄 Syncing...</div>
            
            <div class="container">
                <div class="header">
                    <h1>🔐 5470 Wallet</h1>
                    <p>Blockchain Wallet Inicial</p>
                </div>
                
                <div class="wallet-box">
                    <div class="balance-display">
                        <span id="balance">""" + str(wallet_data["balance"]) + """</span> 5470
                    </div>
                    <div class="address-display">
                        """ + wallet_data["address"] + """
                    </div>
                    
                    <div class="button-grid">
                        <button class="btn btn-send" onclick="sendTokens()">📤 Send</button>
                        <button class="btn btn-receive" onclick="receiveTokens()">📥 Receive</button>
                        <button class="btn btn-mine" onclick="toggleMining()">⛏️ Mining</button>
                        <button class="btn btn-vpn" onclick="toggleVPN()">🌐 VPN</button>
                    </div>
                    
                    <div class="status-panel">
                        <div>Mining: <span id="miningStatus">Inactive</span></div>
                        <div>VPN: <span id="vpnStatus">Disconnected</span></div>
                        <div>Rewards: <span id="rewardsCount">0</span></div>
                    </div>
                    
                    <div class="transactions-panel" id="transactionsPanel">
                        <h4>Recent Transactions</h4>
                        <div class="tx-item">Welcome to 5470 Wallet! 🎉</div>
                    </div>
                </div>
            </div>
            
            <script>
                let mining = false;
                let vpn = false;
                let lastUpdate = Date.now();
                
                // Send Tokens
                function sendTokens() {
                    const amount = prompt("Enter amount to send:");
                    const recipient = prompt("Enter recipient address (or leave empty for demo):");
                    
                    if (amount && parseFloat(amount) > 0) {
                        const recipientAddr = recipient || '5470demo' + Math.random().toString(36).substr(2, 8);
                        
                        fetch('/api/send', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({
                                amount: parseFloat(amount),
                                recipient: recipientAddr
                            })
                        })
                        .then(r => r.json())
                        .then(data => {
                            if (data.success) {
                                showNotification(`✅ Sent ${amount} 5470 to ${recipientAddr.substr(0,10)}...`);
                                updateWalletData();
                            } else {
                                alert('Error: ' + data.message);
                            }
                        })
                        .catch(e => alert('Error: ' + e.message));
                    }
                }
                
                // Receive Tokens
                function receiveTokens() {
                    const address = '""" + wallet_data["address"] + """';
                    const message = `Your 5470 Wallet Address:\\n\\n${address}\\n\\nShare this to receive 5470 tokens!`;
                    
                    if (navigator.clipboard) {
                        navigator.clipboard.writeText(address).then(() => {
                            showNotification('📋 Address copied to clipboard!');
                            alert(message + '\\n\\n✅ Address copied to clipboard!');
                        }).catch(() => {
                            alert(message);
                        });
                    } else {
                        alert(message);
                    }
                }
                
                // Toggle Mining
                function toggleMining() {
                    mining = !mining;
                    
                    fetch('/api/mining/' + (mining ? 'start' : 'stop'), {
                        method: 'POST'
                    })
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('miningStatus').textContent = mining ? 'Active ⛏️' : 'Inactive';
                        showNotification(data.message);
                    })
                    .catch(e => alert('Mining Error: ' + e.message));
                }
                
                // Toggle VPN
                function toggleVPN() {
                    vpn = !vpn;
                    
                    fetch('/api/vpn/' + (vpn ? 'connect' : 'disconnect'), {
                        method: 'POST'
                    })
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('vpnStatus').textContent = vpn ? 'Connected 🌐' : 'Disconnected';
                        showNotification(data.message);
                    })
                    .catch(e => alert('VPN Error: ' + e.message));
                }
                
                // Update Wallet Data
                function updateWalletData() {
                    fetch('/api/status')
                        .then(r => r.json())
                        .then(data => {
                            document.getElementById('balance').textContent = data.balance.toFixed(2);
                            document.getElementById('miningStatus').textContent = data.is_mining ? 'Active ⛏️' : 'Inactive';
                            document.getElementById('vpnStatus').textContent = data.vpn_connected ? 'Connected 🌐' : 'Disconnected';
                            document.getElementById('rewardsCount').textContent = data.mining_rewards;
                            
                            // Update transactions
                            updateTransactions(data.transactions);
                            
                            // Update indicator
                            const indicator = document.getElementById('updateIndicator');
                            indicator.textContent = '✅ Updated';
                            setTimeout(() => {
                                indicator.textContent = '🔄 Syncing...';
                            }, 1000);
                        })
                        .catch(e => console.log('Update error:', e));
                }
                
                // Update Transactions Display
                function updateTransactions(transactions) {
                    const panel = document.getElementById('transactionsPanel');
                    let html = '<h4>Recent Transactions</h4>';
                    
                    if (transactions && transactions.length > 0) {
                        transactions.slice(-5).reverse().forEach(tx => {
                            const sign = tx.type === 'sent' ? '-' : '+';
                            const color = tx.type === 'sent' ? '#e74c3c' : '#27ae60';
                            html += `<div class="tx-item" style="color: ${color}">
                                ${sign} ${tx.amount.toFixed(2)} 5470 - ${tx.type === 'mining' ? 'Mining Reward' : tx.type}
                            </div>`;
                        });
                    } else {
                        html += '<div class="tx-item">Welcome to 5470 Wallet! 🎉</div>';
                    }
                    
                    panel.innerHTML = html;
                }
                
                // Show Notifications
                function showNotification(message) {
                    const notification = document.createElement('div');
                    notification.className = 'notification';
                    notification.textContent = message;
                    document.body.appendChild(notification);
                    
                    setTimeout(() => {
                        notification.remove();
                    }, 3000);
                }
                
                // Auto-update every 3 seconds
                setInterval(updateWalletData, 3000);
                
                // Mining rewards check every 6 seconds
                setInterval(() => {
                    if (mining) {
                        fetch('/api/mining/check', {method: 'POST'})
                            .then(r => r.json())
                            .then(data => {
                                if (data.reward > 0) {
                                    showNotification(`⛏️ Mining Reward: +${data.reward.toFixed(2)} 5470!`);
                                    updateWalletData();
                                }
                            })
                            .catch(e => console.log('Mining check error:', e));
                    }
                }, 6000);
                
                // Initialize on load
                window.onload = function() {
                    updateWalletData();
                    console.log('🔐 5470 Wallet Inicial loaded successfully!');
                };
            </script>
        </body>
        </html>
        """
        
        @app.get("/", response_class=HTMLResponse)
        async def home():
            return html_template
        
        @app.get("/api/status")
        async def get_status():
            wallet_data["last_update"] = datetime.now().isoformat()
            return wallet_data
        
        @app.post("/api/send")
        async def send_tokens(request: Request):
            data = await request.json()
            amount = data.get("amount", 0)
            recipient = data.get("recipient", "unknown")
            
            if amount > wallet_data["balance"]:
                return {"success": False, "message": "Insufficient balance"}
            
            wallet_data["balance"] -= amount
            
            # Add transaction
            tx = {
                "id": str(uuid.uuid4()),
                "recipient": recipient,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "type": "sent"
            }
            wallet_data["transactions"].append(tx)
            
            return {
                "success": True,
                "message": f"Sent {amount} 5470 successfully!",
                "new_balance": wallet_data["balance"]
            }
        
        @app.post("/api/mining/start")
        async def start_mining():
            wallet_data["is_mining"] = True
            return {"message": "⛏️ Mining started successfully!", "success": True}
        
        @app.post("/api/mining/stop")
        async def stop_mining():
            wallet_data["is_mining"] = False
            return {"message": "Mining stopped", "success": True}
        
        @app.post("/api/mining/check")
        async def check_mining():
            if wallet_data["is_mining"]:
                if random.random() < 0.35:  # 35% chance every 6 seconds
                    reward = random.uniform(20.0, 80.0)
                    wallet_data["balance"] += reward
                    wallet_data["mining_rewards"] += 1
                    
                    # Add mining transaction
                    mining_tx = {
                        "id": str(uuid.uuid4()),
                        "recipient": wallet_data["address"],
                        "amount": reward,
                        "timestamp": datetime.now().isoformat(),
                        "type": "mining"
                    }
                    wallet_data["transactions"].append(mining_tx)
                    
                    return {"reward": reward, "message": f"Mining reward: {reward:.2f} 5470!"}
            
            return {"reward": 0}
        
        @app.post("/api/vpn/connect")
        async def connect_vpn():
            wallet_data["vpn_connected"] = True
            return {"message": "🌐 VPN connected successfully!", "success": True}
        
        @app.post("/api/vpn/disconnect")
        async def disconnect_vpn():
            wallet_data["vpn_connected"] = False
            return {"message": "VPN disconnected", "success": True}
        
        print("✅ 5470 Wallet Inicial iniciada")
        print("📍 Accede en: http://localhost:8002")
        print("🔄 Auto-actualización activada")
        print("🛑 Presiona Ctrl+C para parar")
        print("-" * 50)
        
        # Lanzar en puerto 8002 (diferente para evitar conflictos)
        uvicorn.run(app, host="0.0.0.0", port=8002, log_level="warning")
        
    except KeyboardInterrupt:
        print("\n🛑 5470 Wallet detenida")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
