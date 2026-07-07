from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(
    title="GigHub API",
    description="""
    API for managing freelance gigs in Nairobi

    Registration Number: C027-01-0852/2024
    """,
    version="1.0.0"
)

# ------------------------------------------
# Admission Number: C027-01-0852/2024
# Number of Gigs: 7
# Categories: Development, Design, Writing
# Currency: KES
# ------------------------------------------
@app.get("/")
def home():
    return {
        "registration_number": "C027-01-0852/2024"
    }



gigs_db = [
    {
        "id": 1,
        "title": "Build an E-commerce Website",
        "description": "Develop a responsive e-commerce website with payment integration and product management features.",
        "category": "Development",
        "budget": 50000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Design a Company Logo",
        "description": "Create a modern and professional logo together with a complete brand identity package.",
        "category": "Design",
        "budget": 12000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Brian Otieno"
    },
    {
        "id": 3,
        "title": "Write SEO Blog Articles",
        "description": "Write engaging SEO-friendly blog articles for a technology company targeting Kenyan readers.",
        "category": "Writing",
        "budget": 18000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Mercy Wanjiku"
    },
    {
        "id": 4,
        "title": "Develop School Management System",
        "description": "Build a complete school management system with student records, fees and reporting modules.",
        "category": "Development",
        "budget": 85000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Peter Kamau"
    },
    {
        "id": 5,
        "title": "Design Social Media Posters",
        "description": "Create attractive promotional posters for Facebook, Instagram and LinkedIn campaigns.",
        "category": "Design",
        "budget": 9000.0,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Faith Njeri"
    },
    {
        "id": 6,
        "title": "Technical Report Writing",
        "description": "Prepare a detailed technical report for an engineering consultancy project with proper formatting.",
        "category": "Writing",
        "budget": 22000.0,
        "currency": "KES",
        "status": "Open",
        "client_name": "Samuel Mwangi"
    },
    {
        "id": 7,
        "title": "Mobile App Bug Fixes",
        "description": "Fix application bugs, improve performance and optimize user experience for Android devices.",
        "category": "Development",
        "budget": 30000.0,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Ann Wairimu"
    }
]

# ------------------------------------------
# Pydantic Models
# ------------------------------------------

class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=500)
    category: str
    budget: float = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=50)


class GigUpdate(BaseModel):
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[str] = None

    # ------------------------------------------
# GET ALL GIGS
# ------------------------------------------

@app.get("/gigs")
def get_gigs(
    category: Optional[str] = None,
    min_budget: Optional[float] = None,
    max_budget: Optional[float] = None
):
    """
    Retrieve all gigs with optional filtering.
    """

    results = gigs_db

    if category:
        results = [
            gig for gig in results
            if gig["category"].lower() == category.lower()
        ]

    if min_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] >= min_budget
        ]

    if max_budget is not None:
        results = [
            gig for gig in results
            if gig["budget"] <= max_budget
        ]

    return results





# ------------------------------------------
# SEARCH GIGS
# ------------------------------------------

@app.get("/gigs/search")
def search_gigs(q: str):
    """
    Search for gigs by title.
    """

    results = []

    for gig in gigs_db:
        if q.lower() in gig["title"].lower():
            results.append(gig)

    return results
# ------------------------------------------
# GET GIG BY ID
# ------------------------------------------

@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    """
    Retrieve a single gig by its ID.
    """

    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(
        status_code=404,
        detail="Gig not found"
    )



# ------------------------------------------
# CREATE NEW GIG
# ------------------------------------------

@app.post("/gigs")
def create_gig(gig: GigCreate):
    """
    Create a new gig.
    """

    allowed_categories = [
        "Development",
        "Design",
        "Writing"
    ]

    if gig.category not in allowed_categories:
        raise HTTPException(
            status_code=400,
            detail="Invalid category"
        )

    for existing_gig in gigs_db:
        if (
            existing_gig["title"].lower() == gig.title.lower()
            and
            existing_gig["client_name"].lower() == gig.client_name.lower()
        ):
            raise HTTPException(
                status_code=400,
                detail="Gig already exists"
            )

    new_id = max([g["id"] for g in gigs_db]) + 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }
# ------------------------------------------
# UPDATE A GIG
# ------------------------------------------

@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):
    """
    Update a gig's budget or status.
    """

    allowed_statuses = [
        "Open",
        "In Progress",
        "Closed"
    ]

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget

            if gig_update.status is not None:

                if gig_update.status not in allowed_statuses:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid status"
                    )

                gigs_db[index]["status"] = gig_update.status

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(
        status_code=404,
        detail="Gig not found"
    )


# ------------------------------------------
# DELETE A GIG
# ------------------------------------------

@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):
    """
    Delete a gig by its ID.
    """

    for index, gig in enumerate(gigs_db):

        if gig["id"] == gig_id:

            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }

    raise HTTPException(
        status_code=404,
        detail="Gig not found"
    )

