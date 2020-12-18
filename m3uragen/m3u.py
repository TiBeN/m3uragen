"""
m3u module
"""

import os


def generate(software, out_dir, suffix):
    """
    Generate M3U file for the given software into
    out_dir
    """
    m3u_filename = software.name + (suffix if suffix else '') + '.m3u'
    m3u_fd = open(os.path.join(out_dir, m3u_filename), 'w')

    for i in software.images():
        image_rel_path = os.path.relpath(i.path, out_dir)
        m3u_fd.write((image_rel_path + '\n'))

    m3u_fd.close()


def generate_all(softwares, out_dir, suffix):
    """
    Generate M3U file for the list of softwares into
    out_dir
    """
    if not out_dir.exists():
        out_dir.mkdir(parents=True)
    for software in softwares:
        generate(software, out_dir, suffix)
