from fastapi import FastAPI, HTTPException
from app.schemas import CompletionRequest, CompletionResponse, StatsResponse, RoutingConfigUpdate
from app.router_service import RoutingService
from app.config_store import RoutingConfigStore

app = FastAPI(
    title="LLM Cost Autopilot",
    version="1.0.0",
    description="Routing-only completion API with cost optimization",
)

service = RoutingService()
config_store = RoutingConfigStore()


@app.post("/v1/completions", response_model=CompletionResponse)
async def completions(req: CompletionRequest):
    try:
        return await service.complete(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/v1/stats", response_model=StatsResponse)
async def stats():
    return service.stats()


@app.put("/v1/routing-config")
async def update_routing_config(payload: RoutingConfigUpdate):
    updated = config_store.update(payload.model_dump())
    return {"ok": True, "updated_config": updated}


@app.get("/health")
async def health():
    return {"status": "ok"}
