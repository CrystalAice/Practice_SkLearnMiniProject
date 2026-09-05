import base64
import io
from typing import Optional

import matplotlib
matplotlib.use("Agg")  # non-interactive backend, required for servers
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="Seaborn Plot API")


class PlotRequest(BaseModel):
    x: str
    y: str
    kind: str = "scatter"  # scatter, line, bar, hist, box
    hue: Optional[str] = None


@app.get("/")
def root():
    return {"status": "ok", "message": "Seaborn Plot API is running"}


@app.get("/plot")
def get_sample_plot():
    """Returns a sample PNG plot using seaborn's built-in tips dataset."""
    tips = sns.load_dataset("tips")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(data=tips, x="total_bill", y="tip", hue="time", ax=ax)
    ax.set_title("Tips vs Total Bill")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.post("/plot")
def create_plot(req: PlotRequest):
    """Generates a plot from the sample dataset based on request parameters.

    Replace `df = sns.load_dataset("tips")` with your own data source
    (CSV, database query, etc.) as needed.
    """
    df = sns.load_dataset("tips")

    for col in [req.x, req.y, req.hue]:
        if col and col not in df.columns:
            raise HTTPException(status_code=400, detail=f"Unknown column: {col}")

    fig, ax = plt.subplots(figsize=(8, 5))

    plot_fns = {
        "scatter": sns.scatterplot,
        "line": sns.lineplot,
        "bar": sns.barplot,
        "box": sns.boxplot,
    }

    if req.kind not in plot_fns:
        plt.close(fig)
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported kind '{req.kind}'. Choose from {list(plot_fns)}",
        )

    plot_fns[req.kind](data=df, x=req.x, y=req.y, hue=req.hue, ax=ax)
    ax.set_title(f"{req.kind.title()} plot: {req.y} vs {req.x}")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    plt.close(fig)
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")


@app.get("/plot-json")
def get_plot_json():
    """Returns a plot as a base64-encoded PNG embedded in JSON."""
    tips = sns.load_dataset("tips")

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(tips["total_bill"], ax=ax)
    ax.set_title("Distribution of Total Bill")

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
    plt.close(fig)
    buf.seek(0)

    img_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return {"image": f"data:image/png;base64,{img_base64}"}
