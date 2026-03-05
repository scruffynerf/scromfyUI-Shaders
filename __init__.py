"""
Scromfy Shaders - OpenGL Shader Nodes for ComfyUI
"""
import os
import importlib
import logging

logger = logging.getLogger(__name__)

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
WEB_DIRECTORY = "./web"

def load_nodes():
    nodes_dir = os.path.join(os.path.dirname(__file__), "nodes")
    if not os.path.exists(nodes_dir):
        return

    for file in os.listdir(nodes_dir):
        if file.endswith("_node.py") or file.endswith("_nodes.py"):
            node_name = file[:-3]
            try:
                module = importlib.import_module(f".nodes.{node_name}", package=__name__)
                if hasattr(module, "NODE_CLASS_MAPPINGS"):
                    NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                if hasattr(module, "NODE_DISPLAY_NAME_MAPPINGS"):
                    NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
            except Exception as e:
                logger.error(f"Failed to load node module {node_name}: {e}")

    # Load creative API
    try:
        from .nodes.includes.creative_api import setup_creative_api
        setup_creative_api()
    except Exception as e:
        logger.error(f"Failed to load creative API: {e}")

load_nodes()

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]

print(f"🎵 Scromfy Shader Nodes loaded: {len(NODE_CLASS_MAPPINGS)} nodes registered")
