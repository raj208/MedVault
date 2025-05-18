def generate_public_key(aadhar, dob):
    # Assume dob is a Python date object; format it
    dob_str = dob.strftime('%d%m%Y')
    return f"{aadhar}{dob_str}"
