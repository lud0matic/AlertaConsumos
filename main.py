from simplegmail import Gmail
from simplegmail.query import construct_query
from bs4 import BeautifulSoup
import re
import csv
from datetime import datetime

DATE = "2025-07-24"
EXPORT_CSV = True  # Set to False if you don't want to export to CSV

def parse_visa_with_simplegmail():
    """Parse Visa emails using simplegmail"""
    
    # Initialize Gmail client
    gmail = Gmail()
    
    # Build query
    query_params = {
        "sender": "alertas@infomistarjetas.com",
        "after": DATE
    }
    
    # Get messages
    messages = gmail.get_messages(query=construct_query(query_params))
    
    if not messages:
        print("No Visa emails found")
        return []
    
    # Sort messages by date (oldest first)
    messages.sort(key=lambda msg: msg.date)
    
    # Print header
    print(f"{'Establecimiento':<40} {'Monto':<15} {'Cuotas':<8} {'Fecha y Hora'}")
    print("-" * 90)
    
    # Track total and data for CSV
    total = 0.0
    visa_data = []
    
    for message in messages:
        # Try to extract from snippet first (usually available)
        if message.snippet:
            monto_match = re.search(r"\$ ([\d\.,]+)", message.snippet)
            monto = monto_match.group(1) if monto_match else None
            establecimiento_match = re.search(r"establecimiento (.*?),", message.snippet)
            establecimiento = (
                establecimiento_match.group(1) if establecimiento_match else None
            )
            # Extract cuotas
            cuotas_match = re.search(r"(\d+)\s*cuotas?", message.snippet, re.IGNORECASE)
            cuotas = cuotas_match.group(1) if cuotas_match else "1"
            
            if establecimiento or monto:
                # Get timestamp
                timestamp = message.date
                print(f"{establecimiento or 'N/A':<40} ${monto or 'N/A':<14} {cuotas:<8} {timestamp}")
                
                # Add to CSV data
                # Parse timestamp if it's a string
                if isinstance(timestamp, str):
                    fecha = timestamp.split()[0] if ' ' in timestamp else timestamp
                    hora = timestamp.split()[1] if ' ' in timestamp and len(timestamp.split()) > 1 else 'N/A'
                else:
                    fecha = timestamp.strftime('%Y-%m-%d')
                    hora = timestamp.strftime('%H:%M:%S')
                    
                visa_data.append({
                    'Tarjeta': 'VISA',
                    'Establecimiento': establecimiento or 'N/A',
                    'Monto': monto or 'N/A',
                    'Cuotas': cuotas,
                    'Fecha': fecha,
                    'Hora': hora
                })
                
                # Add to total
                if monto:
                    try:
                        # Remove commas and convert to float
                        total += float(monto.replace(',', ''))
                    except ValueError:
                        pass
                continue
        
        # If snippet doesn't have info, try plain text or HTML
        text_content = message.plain or message.html or ""
        
        if text_content:
            monto_match = re.search(r"\$ ([\d\.,]+)", text_content)
            monto = monto_match.group(1) if monto_match else None
            establecimiento_match = re.search(r"establecimiento (.*?),", text_content)
            establecimiento = (
                establecimiento_match.group(1) if establecimiento_match else None
            )
            # Extract cuotas
            cuotas_match = re.search(r"(\d+)\s*cuotas?", text_content, re.IGNORECASE)
            cuotas = cuotas_match.group(1) if cuotas_match else "1"
            
            if establecimiento or monto:
                timestamp = message.date
                print(f"{establecimiento or 'N/A':<40} ${monto or 'N/A':<14} {cuotas:<8} {timestamp}")
                
                # Add to CSV data
                # Parse timestamp if it's a string
                if isinstance(timestamp, str):
                    fecha = timestamp.split()[0] if ' ' in timestamp else timestamp
                    hora = timestamp.split()[1] if ' ' in timestamp and len(timestamp.split()) > 1 else 'N/A'
                else:
                    fecha = timestamp.strftime('%Y-%m-%d')
                    hora = timestamp.strftime('%H:%M:%S')
                    
                visa_data.append({
                    'Tarjeta': 'VISA',
                    'Establecimiento': establecimiento or 'N/A',
                    'Monto': monto or 'N/A',
                    'Cuotas': cuotas,
                    'Fecha': fecha,
                    'Hora': hora
                })
                
                # Add to total
                if monto:
                    try:
                        # Remove commas and convert to float
                        total += float(monto.replace(',', ''))
                    except ValueError:
                        pass
    
    # Print subtotal
    print("-" * 90)
    print(f"{'SUBTOTAL VISA:':<40} ${total:,.2f}")
    
    return visa_data


def parse_mastercard_with_simplegmail():
    """Parse Mastercard emails using simplegmail"""
    
    # Initialize Gmail client
    gmail = Gmail()
    
    # Build query
    query_params = {
        "sender": "mcalertas@mcalertas.com.ar",
        "after": DATE
    }
    
    # Get messages
    messages = gmail.get_messages(query=construct_query(query_params))
    
    if not messages:
        print("No Mastercard emails found")
        return []
    
    # Sort messages by date (oldest first)
    messages.sort(key=lambda msg: msg.date)
    
    # Print header
    print(f"{'Comercio':<40} {'Importe':<15} {'Cuotas':<8} {'Fecha':<12} {'Hora'}")
    print("-" * 90)
    
    # Track total and data for CSV
    total = 0.0
    mastercard_data = []
    
    for message in messages:
        # Get HTML content
        if message.html:
            soup = BeautifulSoup(message.html, 'html.parser')
            
            data = {}
            list_items = soup.find_all('li', type='disc')
            
            for item in list_items:
                text = item.get_text(strip=True)
                
                if 'Comercio:' in text:
                    data['comercio'] = text.split(':', 1)[1].strip()
                elif 'Importe:' in text:
                    data['importe'] = text.split(':', 1)[1].strip()
                elif 'Fecha:' in text:
                    data['fecha'] = text.split(':', 1)[1].strip()
                elif 'Hora:' in text:
                    data['hora'] = text.split(':', 1)[1].strip()
                elif 'Cantidad cuotas:' in text:
                    data['cuotas'] = text.split(':', 1)[1].strip()
            
            if data:
                comercio = data.get('comercio', 'N/A')
                importe = data.get('importe', 'N/A')
                fecha = data.get('fecha', 'N/A')
                hora = data.get('hora', 'N/A')
                cuotas = data.get('cuotas', '01')
                
                print(f"{comercio:<40} ${importe:<14} {cuotas:<8} {fecha:<12} {hora}")
                
                # Add to CSV data
                mastercard_data.append({
                    'Tarjeta': 'MASTERCARD',
                    'Establecimiento': comercio,
                    'Monto': importe,
                    'Cuotas': cuotas,
                    'Fecha': fecha,
                    'Hora': hora
                })
                
                # Add to total
                if importe and importe != 'N/A':
                    try:
                        # Remove commas and convert to float
                        total += float(importe.replace(',', ''))
                    except ValueError:
                        pass
        
        # Alternative: use plain text with regex
        elif message.plain:
            # Extract using regex from plain text
            text = message.plain
            
            comercio_match = re.search(r'Comercio:\s*([^\n]+)', text)
            importe_match = re.search(r'Importe:\s*([\d,\.]+)', text)
            fecha_match = re.search(r'Fecha:\s*(\d{2}/\d{2}/\d{4})', text)
            hora_match = re.search(r'Hora:\s*(\d{2}:\d{2})', text)
            cuotas_match = re.search(r'Cantidad cuotas:\s*(\d+)', text)
            
            if any([comercio_match, importe_match, fecha_match, hora_match]):
                comercio = comercio_match.group(1) if comercio_match else 'N/A'
                importe = importe_match.group(1) if importe_match else 'N/A'
                fecha = fecha_match.group(1) if fecha_match else 'N/A'
                hora = hora_match.group(1) if hora_match else 'N/A'
                cuotas = cuotas_match.group(1) if cuotas_match else '01'
                
                print(f"{comercio:<40} ${importe:<14} {cuotas:<8} {fecha:<12} {hora}")
                
                # Add to CSV data
                mastercard_data.append({
                    'Tarjeta': 'MASTERCARD',
                    'Establecimiento': comercio,
                    'Monto': importe,
                    'Cuotas': cuotas,
                    'Fecha': fecha,
                    'Hora': hora
                })
                
                # Add to total
                if importe and importe != 'N/A':
                    try:
                        # Remove commas and convert to float
                        total += float(importe.replace(',', ''))
                    except ValueError:
                        pass
    
    # Print subtotal
    print("-" * 90)
    print(f"{'SUBTOTAL MASTERCARD:':<40} ${total:,.2f}")
    
    return mastercard_data


def export_to_csv(visa_data, mastercard_data):
    """Export transaction data to CSV file"""
    
    # Combine all data
    all_data = visa_data + mastercard_data
    
    if not all_data:
        print("\nNo data to export to CSV")
        return
    
    # Generate filename with current date
    filename = f"transacciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    # Write to CSV
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Tarjeta', 'Establecimiento', 'Monto', 'Cuotas', 'Fecha', 'Hora']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(all_data)
    
    print(f"\n✓ Datos exportados a: {filename}")
    print(f"  Total de transacciones: {len(all_data)}")


if __name__ == "__main__":
    print("=== VISA ALERTS ===")
    visa_data = parse_visa_with_simplegmail()
    
    print("\n=== MASTERCARD ALERTS ===")
    mastercard_data = parse_mastercard_with_simplegmail()
    
    # Export to CSV if enabled
    if EXPORT_CSV:
        export_to_csv(visa_data, mastercard_data)
