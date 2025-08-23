from fastapi import FastAPI
from pydantic import BaseModel, Field
from time import perf_counter

app = FastAPI(title="Hanoi Backend", version="0.2.0")

# -- JSON Modules --

class Labels(BaseModel):
    from_: str = Field("A", alias="from")
    aux: str = "B"
    to: str = "C"

class SolveRequest(BaseModel):
    # App sends { "n": 5 }, keep the n for contract
    n: int = Field(ge=1, le= 64)
    labels: Labels = Labels()

class Move(BaseModel):
    disk: int
    from_: str = Field(alias="from")
    to: str
class SolveResponse(BaseModel):
    n: int
    count: int
    moves: list[Move] | None = None
    movesOmitted: bool = False
    elapsed_ms: float

# -- domain helper -- 

def generate_moves (n: int, a: str, b: str, c: str, out: list[Move]) -> None:
    if n == 0:
        return
    generate_moves(n-1, a, c, b, out)
    out.append(Move(disk=n, **{"from": a}, to=c))
    generate_moves(n-1, b, a, c, out)

# -- routes -- 

@app.get("/")
def root():
    return {"message": "Hanoi App Backend is running, try GET /health or /docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/solve", response_model = SolveResponse)
def solve(req: SolveRequest) -> SolveResponse:
    start = perf_counter()
    count = (1 << req.n) - 1 # 2**n - 1
    moves: list[Move] | None = None
    moves_omitted = False

    if req.n <= 20:
        buf: list[Move] = []
        generate_moves(req.n, req.labels.from_, req.labels.aux, req.labels.to, buf)
        moves = buf
    else: 
        moves_omitted = True
    elapsed = (perf_counter() - start) * 1000.0

    return SolveResponse(
        n=req.n,
        count=count,
        moves=moves,
        movesOmitted=moves_omitted,
        elapsed_ms=elapsed,
    )