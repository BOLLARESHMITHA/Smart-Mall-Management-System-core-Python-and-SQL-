# src/service/notification_service.py
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_KEY

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

TABLE = "notification"

def create_notification(cust_id, notif_type, message, notify_date):
    supabase.table(TABLE).insert({
        "cust_id": cust_id,
        "type": notif_type,
        "message": message,
        "notify_date": notify_date,
        "read": False
    }).execute()

def get_notifications(cust_id):
    resp = supabase.table(TABLE).select("*").eq("cust_id", cust_id).execute()
    return resp.data

# ✅ Add this function to fix your error
def list_all_notifications():
    resp = supabase.table(TABLE).select("*").execute()
    return resp.data

def mark_as_read(notification_id):
    supabase.table(TABLE).update({"read": True}).eq("id", notification_id).execute()

def filter_notifications(cust_id=None, notif_type=None):
    query = supabase.table("notification").select("*").order("notify_date", desc=True)

    if cust_id is not None and cust_id != -1:
        query = query.eq("cust_id", cust_id)
    if notif_type:
        query = query.eq("type", notif_type)

    resp = query.execute()
    return resp.data or []

