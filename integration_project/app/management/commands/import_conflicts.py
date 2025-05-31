from django.core.management.base import BaseCommand
import csv
from datetime import datetime
from app.models import Conflict

class Command(BaseCommand):
    help = 'Import conflicts from CSV file (conflicts starting after 1960)'
    
    def add_arguments(self, parser):
        parser.add_argument('data/conflicts.csv', type=str, help='Path to CSV file')
        parser.add_argument('--batch-size', type=int, default=1000, 
                          help='Batch size for bulk operations')
    
    def handle(self, *args, **options):
        csv_file = options['data/conflicts.csv']
        batch_size = options['batch_size']
        conflicts_to_create = []
        imported_count = 0
        
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                # Filter by year (after 1960)
                year = int(row['year']) if row['year'] and row['year'].isdigit() else None
                if not year or year <= 1960:
                    continue
                
                # Parse dates safely
                start_date = self.parse_date(row.get('start_date'))
                start_date2 = self.parse_date(row.get('start_date2'))
                ep_end_date = self.parse_date(row.get('ep_end_date'))
                
                # Create conflict instance
                conflict = Conflict(
                    conflict_id=int(row['conflict_id']) if row['conflict_id'] else None,
                    location=row['location'],
                    side_a=row['side_a'],
                    side_a_id=int(row['side_a_id']) if row['side_a_id'] else None,
                    side_a_2nd=row['side_a_2nd'] if row['side_a_2nd'] else None,
                    side_b=row['side_b'],
                    side_b_id=row['side_b_id'],
                    side_b_2nd=row['side_b_2nd'] if row['side_b_2nd'] else None,
                    territory_name=row['territory_name'] if row['territory_name'] else None,
                    year=year,
                    intensity_level=int(row['intensity_level']) if row['intensity_level'] else None,
                    cumulative_intensity=int(row['cumulative_intensity']) if row['cumulative_intensity'] else None,
                    type_of_conflict=int(row['type_of_conflict']) if row['type_of_conflict'] else None,
                    start_date=start_date,
                    start_date2=start_date2,
                    start_prec2=int(row['start_prec2']) if row['start_prec2'] else None,
                    ep_end=int(row['ep_end']) if row['ep_end'] else None,
                    ep_end_date=ep_end_date,
                )
                
                conflicts_to_create.append(conflict)
                
                # Bulk create in batches
                if len(conflicts_to_create) >= batch_size:
                    Conflict.objects.bulk_create(conflicts_to_create, ignore_conflicts=True)
                    imported_count += len(conflicts_to_create)
                    conflicts_to_create = []
                    self.stdout.write(f'Imported {imported_count} conflicts so far...')
            
            # Create remaining conflicts
            if conflicts_to_create:
                Conflict.objects.bulk_create(conflicts_to_create, ignore_conflicts=True)
                imported_count += len(conflicts_to_create)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported {imported_count} conflicts')
        )
    
    def parse_date(self, date_string):
        """Parse date string safely"""
        if not date_string or not date_string.strip():
            return None
        
        # Try different date formats
        formats = ['%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y', '%Y-%m-%d %H:%M:%S']
        for fmt in formats:
            try:
                return datetime.strptime(date_string.strip(), fmt).date()
            except ValueError:
                continue
        return None
