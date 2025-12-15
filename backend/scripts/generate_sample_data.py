"""
Generate realistic sample appointment data for testing
"""

import csv
import random
from datetime import datetime, timedelta

def generate_appointments(num_patients=30, appointments_per_patient=4):
    """
    Generate realistic appointment data.
    
    Creates patterns:
    - Some patients always show up
    - Some patients frequently no-show
    - Some patients are inconsistent
    - Monday mornings have higher no-show rates
    - New patients have higher no-show rates
    """
    
    appointments = []
    
    # Define patient types
    patient_types = {
        'reliable': 0.95,      # 95% show rate
        'mostly_reliable': 0.85,  # 85% show rate
        'inconsistent': 0.60,  # 60% show rate
        'unreliable': 0.30     # 30% show rate
    }
    
    appointment_types = ['cleaning', 'checkup', 'filling', 'extraction', 'root_canal', 'crown']
    
    # Assign patient types
    patients = []
    for i in range(num_patients):
        patient_code = f"P{i+1:03d}"
        
        # Distribution: 40% reliable, 30% mostly reliable, 20% inconsistent, 10% unreliable
        rand = random.random()
        if rand < 0.4:
            patient_type = 'reliable'
        elif rand < 0.7:
            patient_type = 'mostly_reliable'
        elif rand < 0.9:
            patient_type = 'inconsistent'
        else:
            patient_type = 'unreliable'
            
        patients.append({
            'code': patient_code,
            'type': patient_type,
            'show_rate': patient_types[patient_type]
        })
    
    # Generate appointments over past 6 months
    start_date = datetime.now() - timedelta(days=180)
    
    for patient in patients:
        for apt_num in range(appointments_per_patient):
            # Random date in the past 6 months
            days_ago = random.randint(0, 180)
            apt_date = start_date + timedelta(days=days_ago)
            
            # Random time (8 AM - 5 PM, on the hour)
            hour = random.choice([8, 9, 10, 11, 13, 14, 15, 16, 17])
            apt_datetime = apt_date.replace(hour=hour, minute=0, second=0)
            
            # Skip weekends
            if apt_datetime.weekday() >= 5:
                continue
            
            # Determine if they showed up
            base_show_rate = patient['show_rate']
            
            # Adjust for day/time factors
            show_rate = base_show_rate
            
            # Monday mornings have 15% higher no-show rate
            if apt_datetime.weekday() == 0 and hour < 10:
                show_rate -= 0.15
            
            # Friday afternoons are more reliable
            if apt_datetime.weekday() == 4 and hour >= 14:
                show_rate += 0.10
            
            # Early mornings (8 AM) have higher no-show
            if hour == 8:
                show_rate -= 0.10
                
            # First appointment (new patient) has higher no-show
            if apt_num == 0:
                show_rate -= 0.20
            
            # Clamp between 0 and 1
            show_rate = max(0, min(1, show_rate))
            
            # Random determination
            showed_up = random.random() < show_rate
            
            # Random appointment type
            apt_type = random.choice(appointment_types)
            
            appointments.append({
                'patient_code': patient['code'],
                'appointment_datetime': apt_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'showed_up': str(showed_up).lower(),
                'appointment_type': apt_type
            })
    
    return appointments

def save_to_csv(appointments, filename='sample_appointments_large.csv'):
    """Save appointments to CSV file."""
    
    with open(filename, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['patient_code', 'appointment_datetime', 'showed_up', 'appointment_type'])
        writer.writeheader()
        writer.writerows(appointments)
    
    print(f"Generated {len(appointments)} appointments")
    print(f"Saved to {filename}")
    
    # Print stats
    total = len(appointments)
    showed = sum(1 for a in appointments if a['showed_up'] == 'true')
    noshow = total - showed
    
    print(f"\nStats:")
    print(f"  Total appointments: {total}")
    print(f"  Showed up: {showed} ({showed/total*100:.1f}%)")
    print(f"  No-shows: {noshow} ({noshow/total*100:.1f}%)")

if __name__ == '__main__':
    # Generate data
    appointments = generate_appointments(num_patients=50, appointments_per_patient=6)
    
    # Save to CSV
    save_to_csv(appointments, 'sample_appointments_large.csv')
    
    print("\n✅ Done! You can now import this CSV via the API.")