from fastapi import APIRouter
import pandas as pd

router = APIRouter()

# Load the dataset once to improve performance
df = pd.read_csv("../data/hotel_bookings_cleaned.csv")

@router.get("/revenue_trends/")
def get_revenue_trends(year: int, month: str):
    """Returns total revenue for a given year and month."""
    result = df[(df["arrival_date_year"] == year) & (df["arrival_date_month"] == month)]
    
    # Assuming 'adr' (Average Daily Rate) represents revenue per night per booking
    result["total_revenue"] = result["adr"] * result["stays_in_week_nights"] + result["adr"] * result["stays_in_weekend_nights"]
    
    total_revenue = result["total_revenue"].sum()
    return {"year": year, "month": month, "total_revenue": total_revenue}

@router.get("/cancellations/")
def get_cancellations(year: int, month: str, day: int):
    """Returns all canceled bookings for a given date."""
    result = df[(df["arrival_date_year"] == year) & 
                (df["arrival_date_month"] == month) & 
                (df["arrival_date_day_of_month"] == day) & 
                (df["is_canceled"] == 1)]  # Filtering only canceled bookings

    return result.to_dict(orient="records")
