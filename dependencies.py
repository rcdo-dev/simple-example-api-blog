from fastapi import HTTPException, Depends

def check_max_limit(limit: int = 10):
    if limit > 100:
        raise HTTPException(
            status_code=400,
            detail="O limite máximo permitido para posts é 100."
        )
    return limit

def get_current_user(user_id: int = 1):
    return {"user_id": user_id, "username": "admin_simulado"}

def ckeck_admin_permission(current_user: dict = Depends(get_current_user)):
    if current_user["user_id"] != 1:
        raise HTTPException(
            status_code=403,
            detail="Acesso negado: Requer privilegios de administrador."
        )
    return current_user