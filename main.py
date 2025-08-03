from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn
from nlp_parser import parse_description
from repo_analyzer import analyze_repo
from deployer import deploy_with_terraform


app = FastAPI()

class DeployRequest(BaseModel):
    description: str
    repo_url: str

@app.post("/deploy")
async def deploy_app(request: DeployRequest):
    nlp_result = parse_description(request.description)
    repo_result = analyze_repo(request.repo_url)
    deployment_result = deploy_with_terraform(repo_result["path"])

    return {
        "message": "Deployment request received.",
        "description": request.description,
        "repo_url": request.repo_url,
        "parsed": nlp_result,
        "repo_analysis": repo_result,
        "deployment": deployment_result
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
