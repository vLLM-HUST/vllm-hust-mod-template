from importlib.metadata import EntryPoint, distribution
from importlib.resources import files
import json
from types import SimpleNamespace
import unittest


class StarterSmokeTest(unittest.TestCase):
    def test_installed_registration_resolves_to_policy(self):
        installed = distribution("course-vllm-hust-mod")
        entry, = [
            item for item in installed.entry_points
            if item.group == "vllm_hust.extension_bundles"
        ]
        manifest = json.loads(
            files(entry.value).joinpath("vllm-hust-extension-v0.3.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(entry.name, manifest["extension_id"])
        self.assertEqual(installed.version, manifest["extension_version"])

        import_from_manifest = manifest["components"][0]["implementation_ref"]
        implementation = EntryPoint(
            name=entry.name, value=import_from_manifest, group=entry.group
        ).load()
        context = SimpleNamespace(
            candidates=(SimpleNamespace(request_id="a"), SimpleNamespace(request_id="b")),
            builtin_victim_id="b",
            requesting_request_id="a",
            scheduling_policy="fcfs",
            kv_cache_usage=1.0,
            now=1.0,
        )
        self.assertEqual(implementation.vllm_preemption_policy_api_version, 1)
        self.assertIsNone(implementation().select_victim(context))
