#!/usr/bin/env python3
"""
🔐 5470 PROFESSIONAL WALLET - SIMPLIFIED LAUNCH 🔐
Versión profesional sin dependencias complejas
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

def print_professional_banner():
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║                🔐 5470 PROFESSIONAL WALLET 🔐               ║
    ║                                                              ║
    ║  🚀 Professional Blockchain Technology                       ║
    ║  ⛏️  Advanced Mining Engine                                 ║
    ║  🔒 Enhanced Security Features                               ║
    ║  🌐 Professional UI/UX                                      ║
    ║  🎯 MetaMask-style Interface                                ║
    ║                                                              ║
    ║  📍 URL: http://localhost:8001                               ║
    ╚══════════════════════════════════════════════════════════════╝
    """)

def open_browser():
    time.sleep(3)
    try:
        webbrowser.open("http://localhost:8001")
        print("🌐 ¡Navegador abierto! Tu 5470 Professional Wallet está lista!")
    except:
        print("🌐 Abre manualmente: http://localhost:8001")

# Professional Wallet State
wallet_state = {
    "address": "5470_" + hashlib.sha256(str(random.random()).encode()).hexdigest()[:16],
    "balance": 1000.0,
    "transactions": [],
    "is_mining": False,
    "mining_power": 0,
    "privacy_mode": False,
    "vpn_connected": False
}

def main():
    print_professional_banner()
    
    print("🚀 Iniciando 5470 Professional Wallet...")
    print("📡 Cargando características profesionales...")
    
    # Abrir navegador en segundo plano
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    try:
        # Importar FastAPI
        from fastapi import FastAPI, Request
        from fastapi.responses import HTMLResponse
        from fastapi.staticfiles import StaticFiles
        import uvicorn
        
        app = FastAPI(title="5470 Professional Wallet")
        
        # Professional HTML Template
        html_template = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>5470 Professional Wallet</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body { 
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    min-height: 100vh; color: white;
                }
                .container { max-width: 800px; margin: 0 auto; padding: 20px; }
                .header { text-align: center; margin-bottom: 30px; }
                .header h1 { font-size: 2.5em; margin-bottom: 10px; }
                .wallet-card { 
                    background: rgba(255,255,255,0.1); 
                    backdrop-filter: blur(10px);
                    border-radius: 20px; padding: 30px; margin-bottom: 20px;
                    border: 1px solid rgba(255,255,255,0.2);
                }
                .balance { font-size: 2em; text-align: center; margin-bottom: 20px; }
                .address { font-size: 0.9em; opacity: 0.8; text-align: center; margin-bottom: 30px; }
                .buttons { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 15px; }
                .btn { 
                    padding: 15px 20px; border: none; border-radius: 10px; font-size: 16px;
                    cursor: pointer; transition: all 0.3s; font-weight: bold;
                }
                .btn-primary { background: #4CAF50; color: white; }
                .btn-secondary { background: #2196F3; color: white; }
                .btn-warning { background: #FF9800; color: white; }
                .btn-info { background: #9C27B0; color: white; }
                .btn:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.3); }
                .status-bar { 
                    display: flex; justify-content: space-between; align-items: center;
                    background: rgba(0,0,0,0.2); padding: 15px; border-radius: 10px; margin-top: 20px;
                }
                .transactions { margin-top: 20px; }
                .tx-item { 
                    background: rgba(255,255,255,0.1); padding: 10px; border-radius: 5px; 
                    margin-bottom: 10px; font-size: 14px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 5470 Professional Wallet</h1>
                    <p>Advanced Blockchain Technology</p>
                </div>
                
                <div class="wallet-card">
                    <div class="balance">
                        <span id="balance">""" + str(wallet_state["balance"]) + """</span> 5470
                    </div>
                    <div class="address">
                        Address: """ + wallet_state["address"] + """
                    </div>
                    
                    <div class="buttons">
                        <button class="btn btn-primary" onclick="sendTransaction()">📤 Send</button>
                        <button class="btn btn-secondary" onclick="receiveTokens()">📥 Receive</button>
                        <button class="btn btn-warning" onclick="toggleMining()">⛏️ Mining</button>
                        <button class="btn btn-info" onclick="toggleVPN()">🌐 VPN</button>
                    </div>
                    
                    <div class="status-bar">
                        <div>Mining: <span id="mining-status">Inactive</span></div>
                        <div>VPN: <span id="vpn-status">Disconnected</span></div>
                        <div>Privacy: <span id="privacy-status">Standard</span></div>
                    </div>
                    
                    <div class="transactions" id="transactions">
                        <h3>Recent Transactions</h3>
                        <div class="tx-item">+ 50.0 5470 - Mining Reward</div>
                        <div class="tx-item">+ 25.0 5470 - Mining Reward</div>
                    </div>
                </div>
            </div>
            
            <script>
                let mining = false;
                let vpn = false;
                
                function sendTransaction() {
                    const amount = prompt("Enter amount to send:");
                    const recipient = prompt("Enter recipient address (or press OK for demo):");
                    if (amount) {
                        const recipientAddr = recipient || '5470demo' + Math.random().toString(36).substr(2, 9);
                        fetch('/api/wallet/send', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({recipient: recipientAddr, amount: parseFloat(amount)})
                        }).then(r => r.json()).then(data => {
                            alert(data.message || 'Transaction sent!');
                            document.getElementById('balance').textContent = data.new_balance;
                            updateTransactions();
                        }).catch(e => {
                            alert('Error: ' + e.message);
                        });
                    }
                }
                
                function receiveTokens() {
                    const address = '""" + wallet_state["address"] + """';
                    const message = `Your 5470 Professional Wallet Address:\\n\\n${address}\\n\\nShare this address to receive 5470 tokens!`;
                    
                    if (navigator.clipboard) {
                        navigator.clipboard.writeText(address).then(() => {
                            alert(message + '\\n\\n✅ Address copied to clipboard!');
                        }).catch(() => {
                            alert(message);
                        });
                    } else {
                        alert(message);
                    }
                }
                
                function toggleMining() {
                    mining = !mining;
                    fetch('/api/mining/' + (mining ? 'start' : 'stop'), {method: 'POST'})
                        .then(r => r.json()).then(data => {
                            document.getElementById('mining-status').textContent = mining ? 'Active ⛏️' : 'Inactive';
                            alert(data.message);
                        });
                }
                
                function toggleVPN() {
                    vpn = !vpn;
                    fetch('/api/vpn/' + (vpn ? 'connect' : 'disconnect'), {method: 'POST'})
                        .then(r => r.json()).then(data => {
                            document.getElementById('vpn-status').textContent = vpn ? 'Connected 🌐' : 'Disconnected';
                            alert(data.message);
                        }).catch(e => {
                            alert('VPN Error: ' + e.message);
                        });
                }
                
                function updateTransactions() {
                    fetch('/api/wallet/transactions')
                        .then(r => r.json())
                        .then(data => {
                            const txDiv = document.getElementById('transactions');
                            let html = '<h3>Recent Transactions</h3>';
                            
                            if (data.transactions && data.transactions.length > 0) {
                                data.transactions.slice(-5).reverse().forEach(tx => {
                                    const sign = tx.type === 'sent' ? '-' : '+';
                                    html += `<div class="tx-item">${sign} ${tx.amount} 5470 - ${tx.type === 'sent' ? 'Sent to' : 'Received from'} ${tx.recipient || 'Unknown'}</div>`;
                                });
                            } else {
                                html += '<div class="tx-item">+ 50.0 5470 - Mining Reward</div>';
                                html += '<div class="tx-item">+ 25.0 5470 - Mining Reward</div>';
                            }
                            
                            txDiv.innerHTML = html;
                        }).catch(e => {
                            console.log('Transaction update error:', e);
                        });
                }
                
                // Auto-update balance and data every 3 seconds
                function refreshWalletData() {
                    fetch('/api/wallet/status')
                        .then(r => r.json())
                        .then(data => {
                            document.getElementById('balance').textContent = data.balance;
                            document.getElementById('mining-status').textContent = data.is_mining ? 'Active ⛏️' : 'Inactive';
                            document.getElementById('vpn-status').textContent = data.vpn_connected ? 'Connected 🌐' : 'Disconnected';
                            updateTransactions();
                        }).catch(e => console.log('Refresh error:', e));
                }
                
                // Auto-update mining rewards
                setInterval(() => {
                    if (mining) {
                        fetch('/api/mining/reward', {method: 'POST'})
                            .then(r => r.json())
                            .then(data => {
                                if (data.reward) {
                                    document.getElementById('balance').textContent = data.new_balance;
                                    updateTransactions();
                                    // Show reward notification
                                    showNotification(`⛏️ Mining Reward: +${data.reward.toFixed(2)} 5470!`);
                                }
                            }).catch(e => console.log('Mining update error:', e));
                    }
                }, 5000); // Every 5 seconds
                
                // Auto-refresh wallet data every 3 seconds
                setInterval(refreshWalletData, 3000);
                
                // Show notifications
                function showNotification(message) {
                    const notification = document.createElement('div');
                    notification.style.cssText = `
                        position: fixed; top: 20px; right: 20px; background: #4CAF50;
                        color: white; padding: 15px; border-radius: 10px; z-index: 1000;
                        box-shadow: 0 5px 15px rgba(0,0,0,0.3); animation: slideIn 0.5s;
                    `;
                    notification.textContent = message;
                    document.body.appendChild(notification);
                    
                    setTimeout(() => {
                        notification.remove();
                    }, 3000);
                }
                
                window.onload = function() {
                    updateTransactions();
                    refreshWalletData();
                    console.log('🔐 5470 Professional Wallet loaded successfully!');
                };
            </script>
        </body>
        </html>
        """
        
        @app.get("/", response_class=HTMLResponse)
        async def home():
            return html_template
        
        @app.post("/api/wallet/send")
        async def send_transaction(request: Request):
            data = await request.json()
            amount = data.get("amount", 0)
            recipient = data.get("recipient", "unknown")
            
            if amount > wallet_state["balance"]:
                return {"success": False, "message": "Insufficient balance"}
            
            wallet_state["balance"] -= amount
            
            # Add transaction
            tx = {
                "id": str(uuid.uuid4()),
                "recipient": recipient,
                "amount": amount,
                "timestamp": datetime.now().isoformat(),
                "type": "sent"
            }
            wallet_state["transactions"].append(tx)
            
            return {
                "success": True, 
                "message": f"Sent {amount} 5470 to {recipient}",
                "new_balance": wallet_state["balance"]
            }
        
        @app.get("/api/wallet/transactions")
        async def get_transactions():
            return {"transactions": wallet_state["transactions"]}
        
        @app.post("/api/mining/start")
        async def start_mining():
            wallet_state["is_mining"] = True
            return {"message": "Professional mining started! 🚀", "success": True}
        
        @app.post("/api/mining/stop")
        async def stop_mining():
            wallet_state["is_mining"] = False
            return {"message": "Mining stopped", "success": True}
        
        @app.post("/api/mining/reward")
        async def mining_reward():
            if wallet_state["is_mining"]:
                if random.random() < 0.4:  # 40% chance
                    reward = random.uniform(15.0, 75.0)  # Higher rewards
                    wallet_state["balance"] += reward
                    
                    mining_tx = {
                        "id": str(uuid.uuid4()),
                        "recipient": wallet_state["address"],
                        "amount": reward,
                        "timestamp": datetime.now().isoformat(),
                        "type": "mining"
                    }
                    wallet_state["transactions"].append(mining_tx)
                    
                    return {
                        "reward": reward,
                        "new_balance": wallet_state["balance"],
                        "message": f"Professional mining reward: {reward:.2f} 5470!"
                    }
            
            return {"reward": 0, "new_balance": wallet_state["balance"]}
        
        @app.post("/api/vpn/connect")
        async def connect_vpn():
            wallet_state["vpn_connected"] = True
            return {"message": "Professional VPN connected! 🌐", "success": True}
        
        @app.post("/api/vpn/disconnect")
        async def disconnect_vpn():
            wallet_state["vpn_connected"] = False
            return {"message": "VPN disconnected", "success": True}
        
        print("✅ 5470 Professional Wallet iniciada")
        print("📍 Accede a tu wallet en: http://localhost:8001")
        print("🛑 Presiona Ctrl+C para parar")
        print("-" * 60)
        
        # Lanzar en puerto 8001
        uvicorn.run(app, host="0.0.0.0", port=8001, log_level="warning")
        
    except KeyboardInterrupt:
        print("\n🛑 5470 Professional Wallet detenida")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
