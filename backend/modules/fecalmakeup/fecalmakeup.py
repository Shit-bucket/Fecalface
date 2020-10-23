#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import tensorflow as tf
import numpy as np
from fawkes.differentiator import FawkesMaskGeneration
from fawkes.utils import load_extractor, init_gpu, select_target_label, \
     dump_image, reverse_process_cloaked, Faces, load_image

from fawkes.align_face import aligner
from fawkes.utils import get_file

import os
import sys
import json
import logging

logging.basicConfig(level=logging.INFO)


def generate_cloak_images(protector, image_X, target_emb=None):
    cloaked_image_X = protector.attack(image_X, target_emb)
    return cloaked_image_X


class Fawkes(object):
    def __init__(self, feature_extractor, gpu, batch_size):

        self.feature_extractor = feature_extractor
        self.gpu = gpu
        self.batch_size = batch_size
        global sess
        if ("CUDA_VISIBLE_DEVICES" in os.environ):
            os.environ.pop("CUDA_VISIBLE_DEVICES")
        sess = init_gpu(gpu)
        global graph
        graph = tf.get_default_graph()

        model_dir = os.path.join(os.path.expanduser('~'), '.fawkes')
        if not os.path.exists(os.path.join(model_dir, "mtcnn.p.gz")):
            os.makedirs(model_dir, exist_ok=True)
            get_file("mtcnn.p.gz",
                     "http://mirror.cs.uchicago.edu/fawkes/files/mtcnn.p.gz",
                     cache_dir=model_dir,
                     cache_subdir='')

        self.fs_names = [feature_extractor]
        if isinstance(feature_extractor, list):
            self.fs_names = feature_extractor

        self.aligner = aligner(sess)
        self.feature_extractors_ls = [load_extractor(
            name) for name in self.fs_names]

        self.protector = None
        self.protector_param = None

    def mode2param(self, mode):
        if mode == 'min':
            th = 0.002
            max_step = 20
            lr = 40
        elif mode == 'low':
            th = 0.003
            max_step = 50
            lr = 35
        elif mode == 'mid':
            th = 0.005
            max_step = 200
            lr = 20
        elif mode == 'high':
            th = 0.008
            max_step = 500
            lr = 10
        else:
            raise Exception("mode must be one of 'min', 'low', 'mid', " +
                            "'high', 'ultra', 'custom'")
        return th, max_step, lr

    def run_protection(self, unprotected, protected, image, mode='min',
                       th=0.04, sd=1e9, lr=10, max_step=500, batch_size=1,
                       format='png', separate_target=True, debug=False,
                       no_align=False, lang="spanish"):
        th, max_step, lr = self.mode2param(mode)

        current_param = "-".join([str(x) for x in [mode, th, sd, lr, max_step,
                                                   batch_size, format,
                                                   separate_target, debug]])

        img = load_image(unprotected + "/" + image)

        with graph.as_default():
            faces = Faces([unprotected + "/" + image], [img], self.aligner,
                          verbose=1, no_align=no_align)
            original_images = faces.cropped_faces

            if len(original_images) == 0:
                response = {'module': 'makeup',
                            'status': 'No face detected',
                            'd1': 'No face detected',
                            'd2': 'Unhandled error',
                            'd3': 'No face detected'}
                return response
            original_images = np.array(original_images)

            with sess.as_default():
                target_embedding = select_target_label(
                    original_images,
                    self.feature_extractors_ls,
                    self.fs_names)

                if current_param != self.protector_param:
                    self.protector_param = current_param

                    if self.protector is not None:
                        del self.protector

                    self.protector = FawkesMaskGeneration(
                        sess,
                        self.feature_extractors_ls,
                        batch_size=batch_size,
                        mimic_img=True,
                        intensity_range='imagenet',
                        initial_const=sd,
                        learning_rate=lr,
                        max_iterations=max_step,
                        l_threshold=th,
                        verbose=1 if debug else 0,
                        maximize=False,
                        keep_final=False,
                        image_shape=(224, 224, 3))

                protected_images = generate_cloak_images(
                    self.protector,
                    original_images,
                    target_emb=target_embedding)

                faces.cloaked_cropped_faces = protected_images

                final_images = faces.merge_faces(reverse_process_cloaked(
                    protected_images),
                    reverse_process_cloaked(original_images))

        backend_img = protected + "/" + image
        dump_image(final_images[0], backend_img, format=format)

        if (lang == "english"):
            response = {'module': 'makeup',
                        'status': 'MakeUp Ok',
                        'mode': mode,
                        'd1': 'Face attacked',
                        'd2': 'Mode: {}'.format(mode),
                        'd3': 'The face of this avatar has been attacked ' +
                        'and although it looks identical to the original ' +
                        'photo the reality is that you will see that ' +
                        'the face has alterations that make it different ' +
                        'from the original photo.',
                        'backend_img': backend_img}
        else:
            response = {'module': 'makeup',
                        'status': 'MakeUp Ok',
                        'mode': mode,
                        'd1': 'Rostro atacado',
                        'd2': 'Modo: {}'.format(mode),
                        'd3': 'El rostro de este avatar ha sido atacado y ' +
                        'aunque parezca idéntico a la foto original la ' +
                        'realidad es que verá que el rostro tiene altera' +
                        'ciones que la hacen diferente a la foto original.',
                        'backend_img': backend_img}

        response["url_img"] = backend_img[backend_img.find("/static"):]
        return response


def t_makeup_avatar(image_name, lang="spanish"):
    """ Protect face from avatar """

    directory = os.path.dirname(os.path.realpath(__file__))
    root_dir_idx = directory.find("backend")
    image_temp = os.path.join(directory[:root_dir_idx],
                              "backend/static/avatar")
    fecal_temp = os.path.join(directory[:root_dir_idx],
                              "backend/static/makeup")
    logging.info('Checking directories...')
    if (not os.path.isdir(image_temp)):
        os.makedirs(image_temp)
    if (not os.path.isdir(fecal_temp)):
        os.makedirs(fecal_temp)

    logging.info('Face protection...')
    print('Face protection...')

    image_format = image_name.split(".")[1]
    assert image_format in ['png', 'jpg', 'jpeg']
    if image_format == 'jpg':
        image_format = 'jpeg'

    protector = Fawkes('high_extract', 0, 1)
    response = protector.run_protection(image_temp, fecal_temp, image_name,
                                        'mid', format=image_format, lang=lang)
    return response


def output(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    image_name = sys.argv[1]
    result = t_makeup_avatar(image_name)
    output(result)
