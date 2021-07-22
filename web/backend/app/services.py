import json
from collections import defaultdict

from plotly.graph_objs import Figure
from piro.route import SynthesisRoutes
from app.models import RecommendRoutesRequest, RecommendRoutesTask, RecommendRoutesTaskStatus
from app.settings import Settings
import inspect

global_task_store = {}


def route_recommendation_service(request: RecommendRoutesRequest) -> Figure:
    if not request.target_entry_id.startswith("mp"):
        request.target_entry_id = SynthesisRoutes.get_material_id_from_formula(request.target_entry_id)

    #  maybe there's a better way. pull out the corresponding args from the full request
    args_dict = request.dict()
    synthesis_args = inspect.getfullargspec(SynthesisRoutes).args
    synthesis_args_dict = {k: v for k, v in args_dict.items() if k in synthesis_args}
    recommend_routes_args = inspect.getfullargspec(SynthesisRoutes.recommend_routes).args
    recommend_routes_dict = {k: v for k, v in args_dict.items() if k in recommend_routes_args}

    router = SynthesisRoutes(use_cache_database=Settings().use_cache_db, **synthesis_args_dict)
    fig = router.recommend_routes(**recommend_routes_dict)
    return fig


def create_route_recommendation_task(task: RecommendRoutesTask):
    global_task_store[task.task_id] = task
    task.status = RecommendRoutesTaskStatus.STARTED

    # need to use the plotly figure's to_json for JSON friendly data, but bring back to dict to store
    result_dict = json.loads(route_recommendation_service(task.request).to_json())
    task.result = result_dict
    task.status = RecommendRoutesTaskStatus.SUCCESS


def get_route_recommendation_task(task_id: str) -> RecommendRoutesTask:
    return global_task_store.get(task_id, RecommendRoutesTask())
