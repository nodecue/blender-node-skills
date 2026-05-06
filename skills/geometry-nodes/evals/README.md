# Geometry Nodes Skill Activation Evals

This dataset is for trigger-quality regression checks of the `geometry-nodes` skill description.

## File
- `activation.jsonl`: prompts labeled with `should_trigger`.

## Usage
Use this dataset with your internal skill-evaluation runner to track:
- false positives: `should_trigger=false` but skill triggers
- false negatives: `should_trigger=true` but skill does not trigger

## Update Rule
When description text changes, run activation evals before and after the change and keep both reports.
