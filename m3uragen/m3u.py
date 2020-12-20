"""Handle M3U files generation"""

import os
import logging


def generate(software, out_dir, suffix, dry_run):
    """Generate M3U file for the given software into out_dir"""
    m3u_filename = software.name + (suffix if suffix else '') + '.m3u'

    if not dry_run:
        m3u_fd = open(os.path.join(out_dir, m3u_filename), 'w')

    for i in software.images():
        image_rel_path = os.path.relpath(i.path, out_dir)

        if not dry_run:
            m3u_fd.write((image_rel_path + '\n'))

    if not dry_run:
        m3u_fd.close()
    logging.info('Created M3U file for %s (%i image files)', 
                 software.name, len(software.images()))


def generate_all(softwares, out_dir, suffix, dry_run):
    """Generate M3U file for the list of softwares into out_dir"""
    if not dry_run:
        if not out_dir.exists():
            out_dir.mkdir(parents=True)
            
    multi_images_softwares = (x for x in softwares if x.nb_images() > 1)
    for i in multi_images_softwares:
        try:
            generate(i, out_dir, suffix, dry_run)
        except UnicodeEncodeError:
            logging.warning("Unicode error while processing %s", ascii(i.name))
