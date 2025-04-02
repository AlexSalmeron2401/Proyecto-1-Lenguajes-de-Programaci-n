from dataclasses import dataclass, field
from typing import List, Optional

# Clase base para un curso
@dataclass
class Curso:
    nombre: str
    id: str
    
    def to_dict(self):
        return {"nombre": self.nombre, "id": self.id}

@dataclass
class CursoMatematico(Curso):
    nota_examen1: float
    nota_examen2: float
    nota_examen3: float
    nota_tareas: float
    nota_total: float
    
    def to_dict(self):
        base = super().to_dict()
        base.update({
            "tipo": "matematico",
            "nota_examen1": self.nota_examen1,
            "nota_examen2": self.nota_examen2,
            "nota_examen3": self.nota_examen3,
            "nota_tareas": self.nota_tareas,
            "nota_total": self.nota_total
        })
        return base

@dataclass
class CursoCarrera(Curso):
    nota_proyecto1: float
    nota_proyecto2: float
    nota_laboratorios: float
    nota_total: float

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "tipo": "carrera",
            "nota_proyecto1": self.nota_proyecto1,
            "nota_proyecto2": self.nota_proyecto2,
            "nota_laboratorios": self.nota_laboratorios,
            "nota_total": self.nota_total
        })
        return base

@dataclass
class CursoIngles(Curso):
    nota_examen1: float
    nota_examen2: float
    nota_laboratorios: float
    nota_tareas: float
    nota_total: float

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "tipo": "ingles",
            "nota_examen1": self.nota_examen1,
            "nota_examen2": self.nota_examen2,
            "nota_laboratorios": self.nota_laboratorios,
            "nota_tareas": self.nota_tareas,
            "nota_total": self.nota_total
        })
        return base

@dataclass
class CursoOtros(Curso):
    nota_trabajo1: float
    nota_trabajo2: float
    nota_trabajo3: float
    notas_tareas: float
    nota_total: float

    def to_dict(self):
        base = super().to_dict()
        base.update({
            "tipo": "otroCurso",
            "nota_trabajo1": self.nota_trabajo1,
            "nota_trabajo2": self.nota_trabajo2,
            "nota_trabajo3": self.nota_trabajo3,
            "nota_tareas": self.notas_tareas,
            "nota_total": self.nota_total
        })
        return base

# Clase Semestre: cada semestre tiene un número (1 o 2), una lista de cursos y opcionalmente un profesor
@dataclass
class Semestre:
    semestre: int
    cursos: List[Curso] = field(default_factory=list)
    profesor: Optional["Profesor"] = None

    def to_dict(self):
        return {
            "semestre": self.semestre,
            "cursos": [curso.to_dict() for curso in self.cursos],
            "profesor": self.profesor.to_dict() if self.profesor else None
        }

# Clase Año: contiene el año y dos semestres (por defecto se crean dos instancias de Semestre)
@dataclass
class Ano:
    ano: int
    semestres: List[Semestre] = field(default_factory=lambda: [Semestre(semestre=1), Semestre(semestre=2)])
    
    def to_dict(self):
        return {
            "ano": self.ano,
            "semestres": [semestre.to_dict() for semestre in self.semestres]
        }

# Clase Profesor: ahora incluye email y password; ya no se usa "partner"
@dataclass
class Profesor:
    nombre: str
    id: str
    email: str
    password: str
    anos: List[Ano] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "anos": [ano.to_dict() for ano in self.anos]
        }

# Para modelar la información de un curso que llevó un estudiante, se usa una clase auxiliar
@dataclass
class CursoCursado:
    curso: Curso
    ano: int
    semestre: int
    profesor: Profesor
    
    def to_dict(self):
        return {
            "curso": self.curso.to_dict(),
            "ano": self.ano,
            "semestre": self.semestre,
            "profesor": self.profesor.to_dict()
        }

# Clase Estudiante: ahora incluye email y password, además de nombre, id y la lista de cursos cursados
@dataclass
class Estudiante:
    nombre: str
    id: str
    email: str
    password: str
    cursos_cursados: List[CursoCursado] = field(default_factory=list)
    
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "cursos_cursados": [curso.to_dict() for curso in self.cursos_cursados]
        }
