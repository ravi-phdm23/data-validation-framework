#!/usr/bin/env python3
"""
Fix Streamlit App Syntax Issues
"""

def fix_streamlit_syntax():
    """Fix the syntax issues in streamlit_app.py"""
    
    with open('streamlit_app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the duplicate except blocks and encoding issues
    problematic_section = '''        except Exception as e:
            st.error(f"❌ Error processing Excel file: {str(e)}")
            st.info("� Make sure your Excel file has the required columns and format.")
            
            except Exception as e:
                st.error(f"❌ Error reading Excel file: {str(e)}")
                st.info("Please ensure the Excel file follows the correct format")'''
    
    fixed_section = '''            except Exception as e:
                st.error(f"❌ Error reading Excel file: {str(e)}")
                st.info("Please ensure the Excel file follows the correct format")'''
    
    # Replace the problematic section
    if problematic_section in content:
        content = content.replace(problematic_section, fixed_section)
        print("✅ Fixed duplicate except blocks")
    else:
        print("⚠️ Problematic section not found, trying alternative fix")
        # Try to fix any remaining issues
        lines = content.split('\n')
        fixed_lines = []
        skip_next = False
        
        for i, line in enumerate(lines):
            if skip_next:
                skip_next = False
                continue
                
            # Fix the encoding issues
            line = line.replace('âŒ', '❌').replace('ï¿½', '💡').replace('ðŸ'†', '👆').replace('ðŸ"–', '📖')
            
            # Fix duplicate except blocks
            if 'except Exception as e:' in line and i > 0:
                # Check if previous lines have issues
                prev_lines = lines[max(0, i-5):i]
                if any('except Exception as e:' in prev_line for prev_line in prev_lines):
                    # Skip this duplicate except
                    continue
            
            fixed_lines.append(line)
        
        content = '\n'.join(fixed_lines)
    
    # Write the fixed content
    with open('streamlit_app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Fixed streamlit_app.py syntax issues")

if __name__ == "__main__":
    fix_streamlit_syntax()
