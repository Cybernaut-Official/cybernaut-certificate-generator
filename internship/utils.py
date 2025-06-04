import pandas as pd
from .models import Intern, Certificate, InternshipRole

def process_intern_excel(file, role_id):
    try:
        df = pd.read_excel(file)
        role = InternshipRole.objects.select_related('batch__internship').get(id=role_id)
        internship = role.batch.internship

        existing_ids = {i.intern_id for i in Intern.objects.filter(internship_role=role)}
        interns_to_create = []
        certificates_to_create = []

        for _, row in df.iterrows():
            # Validate required fields
            if pd.isna(row["Email"]) or pd.isna(row["Intern ID"]) or pd.isna(row["Unique Code"]):
                continue

            intern_id = row["Intern ID"]
            unique_code = str(row["Unique Code"]).strip().upper()

            # Skip duplicates
            if intern_id in existing_ids:
                continue

            intern = Intern(
                intern_id=intern_id,
                name=row["Name"],
                email=row["Email"],
                internship_role=role,
            )
            interns_to_create.append(intern)

        # Save interns
        saved_interns = Intern.objects.bulk_create(interns_to_create)

        for intern in saved_interns:
            matching_row = df[df["Intern ID"] == intern.intern_id].iloc[0]
            unique_code = str(matching_row["Unique Code"]).strip().upper()

            certificates_to_create.append(Certificate(
                intern=intern,
                unique_code=unique_code,
                internship_start_date=internship.start_date,
                internship_end_date=internship.end_date,
            ))

        Certificate.objects.bulk_create(certificates_to_create)

        return {"success": f"{len(saved_interns)} interns added and certificates generated."}

    except Exception as e:
        return {"error": str(e)}
