import os
import getpass
import pikepdf

def print_banner():
    print("=" * 60)
    print("🔐 ALPHA's PDF FILE LOCK & UNLOCK TOOL 🔐".center(60))
    print("=" * 60)

def ask_mode():
    print("\nChoose an option:")
    print("1️⃣   Lock (Protect) a PDF")
    print("2️⃣   Unlock (Remove password from) a PDF")
    choice = input("\nEnter 1 or 2: ").strip()
    if choice not in ['1', '2']:
        print("❌ Invalid choice!")
        exit(1)
    return choice

def ask_file_path():
    file_path = input("📂 Enter full path of the PDF: ").strip()
    if not os.path.isfile(file_path):
        print("❌ File not found!")
        exit(1)
    ext = os.path.splitext(file_path)[1].lower()
    if ext != '.pdf':
        print("❌ Only PDF files are supported!")
        exit(1)
    return file_path

def ask_password(prompt="🔑 Enter password: "):
    return getpass.getpass(prompt)

def ask_save_location(suffix=".pdf"):
    output_dir = input("📁 Enter directory to save the new PDF: ").strip()
    if not os.path.isdir(output_dir):
        print("❌ Directory not found!")
        exit(1)
    output_name = input("📝 What should the saved file be named (without extension)? ").strip()
    return os.path.join(output_dir, output_name + suffix)

def protect_pdf(file_path, password, output_path):
    try:
        pdf = pikepdf.open(file_path)
        pdf.save(output_path, encryption=pikepdf.Encryption(owner=password, user=password, R=6))
        pdf.close()
        print(f"✅ Protected PDF saved at: {output_path}")
    except Exception as e:
        print(f"❌ Error protecting PDF: {e}")

def unlock_pdf(file_path, password, output_path):
    try:
        pdf = pikepdf.open(file_path, password=password)
        pdf.save(output_path)
        pdf.close()
        print(f"✅ Unlocked PDF saved at: {output_path}")
    except pikepdf.PasswordError:
        print("❌ Incorrect password!")
    except Exception as e:
        print(f"❌ Error unlocking PDF: {e}")

def is_pdf_encrypted(file_path):
    try:
        with open(file_path, 'rb') as f:
            pdf = pikepdf.open(f)
            pdf.close()
            return False
    except pikepdf.PasswordError:
        return True
    except Exception:
        return False  # Possibly corrupted or invalid PDF

def main():
    print_banner()
    mode = ask_mode()
    file_path = ask_file_path()

    if mode == '1':  # Lock
        if is_pdf_encrypted(file_path):
            print("❌ This PDF is already password-protected!")
            exit(1)
        password = ask_password("🔑 Enter a strong password to lock the PDF: ")
        confirm = ask_password("🔑 Confirm password: ")
        if password != confirm:
            print("❌ Passwords do not match!")
            exit(1)
        output_path = ask_save_location()
        print("\n🔐 Locking your PDF...")
        protect_pdf(file_path, password, output_path)

    elif mode == '2':  # Unlock
        if not is_pdf_encrypted(file_path):
            print("ℹ️ This PDF is not password-protected.")
            exit(0)
        password = ask_password("🔑 Enter the current password to unlock the PDF: ")
        output_path = ask_save_location()
        print("\n🔓 Unlocking your PDF...")
        unlock_pdf(file_path, password, output_path)

    print("\n🎉 Done!\n\n\n")

if __name__ == "__main__":
    main()
