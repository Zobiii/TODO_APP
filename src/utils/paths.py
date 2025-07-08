import os, sys


def resource_path(relative_path):
    """Pfad zu Ressourcen – funktioniert auch im gepackten Zustand mit PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.abspath("./src"))
    return os.path.join(base_path, relative_path)
