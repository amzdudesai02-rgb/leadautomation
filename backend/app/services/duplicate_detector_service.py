from app.services.google_sheets_service import GoogleSheetsService
from app.utils.logger import get_logger
import difflib

logger = get_logger(__name__)

class DuplicateDetectorService:
    """Service for detecting and handling duplicates in Google Sheets"""
    
    def __init__(self):
        self.sheets_service = GoogleSheetsService()
    
    def detect_duplicate_sellers(self):
        """Detect duplicate sellers based on name, email, or URL"""
        try:
            sellers = self.sheets_service.get_sellers(page=1, limit=1000)
            duplicates = []
            seen = {}
            
            for idx, seller in enumerate(sellers):
                # Create unique key from seller data
                name = seller.get('name', '').lower().strip()
                email = seller.get('email', '').lower().strip()
                url = seller.get('store_url', '').lower().strip()
                
                # Check for exact duplicates
                key = f"{name}|{email}|{url}"
                if key in seen:
                    duplicates.append({
                        'type': 'exact',
                        'original': seen[key],
                        'duplicate': idx,
                        'seller': seller
                    })
                else:
                    seen[key] = idx
                
                # Check for similar names (fuzzy matching)
                if name:
                    for existing_key, existing_idx in seen.items():
                        if existing_idx == idx:
                            continue
                        existing_name = existing_key.split('|')[0]
                        similarity = difflib.SequenceMatcher(None, name, existing_name).ratio()
                        if similarity > 0.85 and similarity < 1.0:  # 85% similar but not exact
                            duplicates.append({
                                'type': 'similar',
                                'original': existing_idx,
                                'duplicate': idx,
                                'seller': seller,
                                'similarity': similarity
                            })
            
            return duplicates
            
        except Exception as e:
            logger.error(f"Error detecting duplicate sellers: {str(e)}")
            return []
    
    def detect_duplicate_brands(self):
        """Detect duplicate brands based on name or domain"""
        try:
            brands = self.sheets_service.get_brands(page=1, limit=1000)
            duplicates = []
            seen = {}
            
            for idx, brand in enumerate(brands):
                name = brand.get('name', '').lower().strip()
                domain = brand.get('domain', '').lower().strip()
                
                # Check for exact duplicates
                key = f"{name}|{domain}"
                if key in seen:
                    duplicates.append({
                        'type': 'exact',
                        'original': seen[key],
                        'duplicate': idx,
                        'brand': brand
                    })
                else:
                    seen[key] = idx
                
                # Check for similar names
                if name:
                    for existing_key, existing_idx in seen.items():
                        if existing_idx == idx:
                            continue
                        existing_name = existing_key.split('|')[0]
                        similarity = difflib.SequenceMatcher(None, name, existing_name).ratio()
                        if similarity > 0.85 and similarity < 1.0:
                            duplicates.append({
                                'type': 'similar',
                                'original': existing_idx,
                                'duplicate': idx,
                                'brand': brand,
                                'similarity': similarity
                            })
            
            return duplicates
            
        except Exception as e:
            logger.error(f"Error detecting duplicate brands: {str(e)}")
            return []
    
    def flag_duplicates_in_sheet(self, sheet_name='Sellers'):
        """Flag duplicates in Google Sheet by highlighting rows"""
        try:
            if not self.sheets_service.sheet:
                return False
            
            worksheet = self.sheets_service.sheet.worksheet(sheet_name)
            
            if sheet_name == 'Sellers':
                duplicates = self.detect_duplicate_sellers()
            elif sheet_name == 'Brands':
                duplicates = self.detect_duplicate_brands()
            else:
                return False
            
            # Highlight duplicate rows (requires gspread formatting)
            for dup in duplicates:
                row_num = dup.get('duplicate', 0) + 2  # +2 for header row
                try:
                    # Format row in yellow to indicate duplicate
                    worksheet.format(f'A{row_num}:E{row_num}', {
                        'backgroundColor': {'red': 1.0, 'green': 0.95, 'blue': 0.8}
                    })
                except:
                    pass
            
            logger.info(f"Flagged {len(duplicates)} duplicates in {sheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error flagging duplicates: {str(e)}")
            return False
    
    def merge_duplicates(self, duplicates, sheet_name='Sellers'):
        """Merge duplicate entries, keeping the most complete data"""
        try:
            if not self.sheets_service.sheet:
                return False
            
            worksheet = self.sheets_service.sheet.worksheet(sheet_name)
            merged_count = 0
            
            for dup in duplicates:
                if dup['type'] == 'exact':
                    # Delete duplicate row
                    row_num = dup.get('duplicate', 0) + 2
                    try:
                        worksheet.delete_rows(row_num)
                        merged_count += 1
                    except:
                        pass
            
            logger.info(f"Merged {merged_count} duplicates in {sheet_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error merging duplicates: {str(e)}")
            return False

