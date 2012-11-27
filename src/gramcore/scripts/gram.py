"""Command line tool to execute a set of pythogram tasks."""
import sys
import json
import logging
from gramcore.datasets import images as dt_images
from gramcore.datasets import surfaces as dt_surfaces
from gramcore.operations import arrays as ops_arrays
from gramcore.operations import images as ops_images


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('gramcore')


MAPPING = {
    'datasets.images.synthetic': dt_images.synthetic,
    'datasets.images.tiled': dt_images.tiled,
    'datasets.surfaces.dtm': dt_surfaces.dtm,
    'operations.arrays.add_noise': ops_arrays.add_noise,
    'operations.arrays.asarray': ops_arrays.asarray,
    'operations.arrays.load': ops_arrays.load,
    'operations.arrays.save': ops_arrays.save,
    'operations.images.fromarray': ops_images.fromarray,
    'operations.images.load': ops_images.load,
    'operations.images.resize': ops_images.resize,
    'operations.images.rotate': ops_images.rotate,
    'operations.images.save': ops_images.save,
}


def get_args(json_file):
    """Parses JSON files.

    It performs a series of checks to ensure everything is fine with the JSON
    input. It is basically a helper for main().
    """
    try:
        json_data = open(json_file).read()
        args = json.loads(json_data)
    except IndexError:
        logger.error("features requires input from a JSON task file.")
        raise
    except IOError:
        logger.error("Cannot find input task file %s", json_file)
        raise
    except ValueError:
        logger.error("Input task file %s is not in valid JSON format.",
                     json_file)
        raise

    try:
        args['tasks']
    except KeyError:
        logger.error("JSON job file must contain a tasks section.")
        raise
    if len(args['tasks']) <= 0:
        logger.warning("Task section empty. No tasks will be performed")

    return args


def gram():
    """Parses JSON input and executes a series of tasks.

    It loops through the JSON project file and for each provided task::

        1. It gets the function object corresponding to the task, based on the
        MAPPING
        2. It gets the provided parameters
        3. It executes the task with the parameters and appends the returned
        results to a list

    The results list is used so that during execution every function can get
    input from previously executed ones.

    In the JSON file when a function needs input from a previous one it uses
    parameters['input_index']. This is always a list e.g. [1, 2]. Every number
    in the list is an index to a function in the JSON file.

    main() loops through parameters['input_index'] and gets the proper data
    from the results list. It then executes the task parsing data to a new
    dictionary entry parameters['data']. Each function knows how to handle the
    provided input.
    """
    args = get_args(sys.argv[1])
    results = []

    for arg in args['tasks']:
        task = MAPPING[arg['task']]
        parameters = arg['parameters']
        # TODO: this should be made a log with logger.debug(....)
        # now it doesn't seem to work
        print "Executing function: ", parameters['task']
        if 'input_index' in parameters:
            data = []
            for input_index in parameters['input_index']:
                data.append(results[input_index])
            parameters['data'] = data

        results.append(task(parameters))

    return True
