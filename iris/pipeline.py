import kfp
import kfp.components as comp
from kfp import dsl
@dsl.pipeline(
    name='test-iris-ver2',
    description='iris test2 No Cache'
)
def test_pipeline():
    add_p = dsl.ContainerOp(
        name="load iris data pipeline",
        image="HPCNFS1:5000/test-iris-preprocessing:0.7",
        arguments=[
            '--data_path', './Iris.csv'
        ],
        file_outputs={'iris' : '/iris.csv'}
    )
    add_p.execution_options.caching_strategy.max_cache_staleness="P0D"
    ml = dsl.ContainerOp(
        name="training pipeline",
        image="HPCNFS1:5000/test-iris-train:0.6",
        arguments=[
            '--data', add_p.outputs['iris']
        ]
    )
    ml.execution_options.caching_strategy.max_cache_staleness="P0D"

    ml.after(add_p)
    
if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(test_pipeline, __file__ + ".tar.gz")

