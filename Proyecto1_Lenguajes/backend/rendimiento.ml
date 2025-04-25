open Yojson.Basic.Util
open Str

(* ------------------------------------------------------------------------------------------------------------------ *)
(* ---------------------------------------------- FUNCIONES GENERALES ----------------------------------------------- *)
(* ------------------------------------------------------------------------------------------------------------------ *)

let string_contains_substring sub s =
  try ignore (Str.search_forward (Str.regexp_string sub) s 0); true
  with Not_found -> false
;;

let promedio_notas notas =
  let total = List.fold_left (+.) 0.0 notas in
  if notas = [] then 0.0 else total /. float_of_int (List.length notas)
;;

let extraer_temas_agregados notas =
  notas
  |> to_assoc
  |> List.filter (fun (clave, valor) ->
      string_contains_substring "tema" (String.lowercase_ascii clave)
      && to_float_option valor <> None)
  |> List.map (fun (clave, valor) ->
      let tema =
        try
          let regex = Str.regexp "\\(tema[0-9]+\\)" in
          ignore (Str.search_forward regex clave 0);
          Str.matched_string clave
        with Not_found -> clave
      in
      (tema, to_float valor)
  )
;;

let agrupar_por_tema_general pares =
  pares
  |> List.map fst
  |> List.sort_uniq String.compare
  |> List.map (fun tema ->
      let notas =
        pares
        |> List.filter (fun (t, _) -> t = tema)
        |> List.map snd
      in
      (tema, promedio_notas notas)
    )
;;

let promedio_por_tipo tipo notas =
  notas
  |> to_assoc
  |> List.filter (fun (clave, valor) ->
      String.contains clave tipo.[0] && to_float_option valor <> None)
  |> List.map (fun (_, valor) -> to_float valor)
  |> promedio_notas
;;

let promedio_general notas =
  let claves = ["notaGeneral"; "notaTotal"; "totaTotal"] in
  notas
  |> to_assoc
  |> List.filter (fun (clave, valor) ->
      List.exists (fun c -> clave = c) claves && to_float_option valor <> None)
  |> List.map (fun (_, valor) -> to_float valor)
  |> promedio_notas
;;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* ------------------------------------------------ VISTA ESTUDIANTE ------------------------------------------------ *)
(* ------------------------------------------------------------------------------------------------------------------ *)

let rendimiento_por_tema_estudiante json =
  json
  |> member "estudiante"
  |> member "cursos"
  |> to_list
  |> List.map (fun curso ->
      let nombre_curso = curso |> member "nombre" |> to_string in
      curso |> member "estudiantes" |> to_list
      |> List.map (fun estudiante ->
          let nombre = estudiante |> member "nombre" |> to_string in
          let notas = estudiante |> member "notas" in
          let temas = extraer_temas_agregados notas in
          let resumen = agrupar_por_tema_general temas in
          (nombre, nombre_curso, resumen)
      )
  )
  |> List.flatten
;;

let resultado_a_json (datos : (string * float) list) : Yojson.Basic.t =
  `Assoc (List.map (fun (clave, valor) -> (clave, `Float valor)) datos)

let guardar_resultado_en_json ruta datos =
  let json = resultado_a_json datos in
  Yojson.Basic.to_file ruta json

let rendimiento_por_curso_estudiante json =
  json
  |> member "estudiante"
  |> member "cursos"
  |> to_list
  |> List.map (fun curso ->
      let nombre_curso = curso |> member "nombre" |> to_string in
      curso
      |> member "estudiantes"
      |> to_list
      |> List.map (fun estudiante ->
          let nombre = estudiante |> member "nombre" |> to_string in
          let notas = estudiante |> member "notas" in

          let resumen =
            ["general"; "examen"; "lab"; "proyecto"; "tarea"; "trabajo"; "presentacion"]
            |> List.filter (fun tipo ->
                if tipo = "general" then true
                else
                  notas
                  |> to_assoc
                  |> List.exists (fun (clave, _) ->
                      String.contains (String.lowercase_ascii clave) tipo.[0]
                      && string_contains_substring tipo (String.lowercase_ascii clave)
                    )
              )
            |> List.map (fun tipo ->
                let valor =
                  if tipo = "general" then promedio_general notas
                  else promedio_por_tipo tipo notas
                in
                let nombre_clave = if tipo = "general" then "general" else tipo ^ "s" in
                (nombre_clave, valor)
              )
          in

          (nombre, nombre_curso, resumen)
      )
  )
  |> List.flatten
;;
  
let rendimiento_por_semestre_estudiante json =
  json
  |> member "estudiante"
  |> member "cursos"
  |> to_list
  |> List.map (fun curso ->
      let semestre = curso |> member "semestre" |> to_int in
      curso
      |> member "estudiantes"
      |> to_list
      |> List.map (fun est ->
          (est |> member "nombre" |> to_string,
           semestre,
           est |> member "notas" |> promedio_general)
      )
  )
  |> List.flatten
  |> fun registros ->
      registros
      |> List.map (fun (n, s, _) -> (n, s))
      |> List.sort_uniq compare
      |> List.map (fun (nombre, semestre) ->
          registros
          |> List.filter (fun (n, s, _) -> n = nombre && s = semestre)
          |> List.map (fun (_, _, prom) -> prom)
          |> promedio_notas
          |> fun prom -> (nombre, semestre, prom)
        )
;;

let rendimiento_por_anio_con_desgloce json =
  json
  |> member "estudiante"
  |> member "cursos"
  |> to_list
  |> List.map (fun curso ->
      let anio = curso |> member "anio" |> to_int in
      let semestre = curso |> member "semestre" |> to_int in
      curso |> member "estudiantes" |> to_list
      |> List.map (fun est ->
          (est |> member "nombre" |> to_string,
           anio,
           semestre,
           est |> member "notas" |> promedio_general)
      )
  )
  |> List.flatten
  |> fun registros ->
      registros
      |> List.map (fun (n, a, _, _) -> (n, a))
      |> List.sort_uniq compare
      |> List.map (fun (nombre, anio) ->
          registros
          |> List.filter (fun (n, a, _, _) -> n = nombre && a = anio)
          |> List.map (fun (_, _, sem, prom) -> (sem, prom))
          |> fun desgloce ->
              (nombre, anio, promedio_notas (List.map snd desgloce), desgloce)
        )
;;

let rendimiento_historico_estudiante por_anio =
  por_anio
  |> List.map (fun (nombre, _, _, _) -> nombre)
  |> List.sort_uniq String.compare
  |> List.map (fun nombre ->
      let desgloce =
        por_anio
        |> List.filter (fun (n, _, _, _) -> n = nombre)
        |> List.map (fun (_, anio, prom, _) -> (anio, prom))
      in
      (nombre,
       desgloce |> List.map snd |> promedio_notas,
       desgloce)
    )
;;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* ------------------------------------------------- VISTA PROFESOR ------------------------------------------------- *)
(* ------------------------------------------------------------------------------------------------------------------ *)

let rendimiento_por_tema_profesor json =
  json
  |> member "estudiante"
  |> member "cursos"
  |> to_list
  |> List.map (fun curso ->
      let nombre_curso = curso |> member "nombre" |> to_string in
      let profesor = curso |> member "profe" |> to_string in
      curso
      |> member "estudiantes"
      |> to_list
      |> List.map (fun est -> est |> member "notas" |> extraer_temas_agregados)
      |> List.flatten
      |> agrupar_por_tema_general
      |> fun resumen -> (profesor, nombre_curso, resumen)
  )
;;

let rendimiento_por_curso_profesor json =
  json
  |> member "estudiante"
  |> member "cursos"
  |> to_list
  |> List.map (fun curso ->
      let nombre_curso = curso |> member "nombre" |> to_string in
      let profesor = curso |> member "profe" |> to_string in
      let estudiantes = curso |> member "estudiantes" |> to_list in
      let notas_estudiantes = List.map (fun e -> e |> member "notas") estudiantes in

      let resumen =
        ["general"; "examen"; "lab"; "proyecto"; "tarea"; "trabajo"; "presentacion"]
        |> List.filter (fun tipo ->
            tipo = "general" ||
            notas_estudiantes
            |> List.exists (fun notas ->
                notas
                |> to_assoc
                |> List.exists (fun (clave, _) ->
                    String.contains (String.lowercase_ascii clave) tipo.[0]
                    && string_contains_substring tipo (String.lowercase_ascii clave)
                  )
              )
          )
        |> List.map (fun tipo ->
            let promedio =
              notas_estudiantes
              |> List.map (fun notas ->
                  if tipo = "general" then promedio_general notas
                  else promedio_por_tipo tipo notas)
              |> promedio_notas
            in
            let tipo_plural = if tipo = "general" then "general" else tipo ^ "s" in
            (tipo_plural, promedio)
          )
      in

      let promedios_generales = List.map promedio_general notas_estudiantes in
      let total = float_of_int (List.length promedios_generales) in
      let aprobados =
        List.filter (fun p -> p >= 70.0) promedios_generales |> List.length |> float_of_int
      in
      let reprobados = total -. aprobados in
      let porcentaje_aprobados = if total = 0.0 then 0.0 else (aprobados /. total) *. 100.0 in
      let porcentaje_reprobados = if total = 0.0 then 0.0 else (reprobados /. total) *. 100.0 in

      let resumen_con_metricas =
        resumen @ [
          ("aprobados", porcentaje_aprobados);
          ("reprobados", porcentaje_reprobados)
        ]
      in

      (profesor, nombre_curso, resumen_con_metricas)
  )
;;

let rendimiento_por_semestre_profesor json =
  json
  |> member "estudiante"
  |> member "cursos"
  |> to_list
  |> List.map (fun curso ->
      let profesor = curso |> member "profe" |> to_string in
      let semestre = curso |> member "semestre" |> to_int in
      curso
      |> member "estudiantes"
      |> to_list
      |> List.map (fun est ->
          let promedio = est |> member "notas" |> promedio_general in
          (profesor, semestre, promedio)
        )
  )
  |> List.flatten
  |> fun registros ->
      registros
      |> List.map (fun (p, s, _) -> (p, s))
      |> List.sort_uniq compare
      |> List.map (fun (profe, semestre) ->
          let datos =
            registros
            |> List.filter (fun (p, s, _) -> p = profe && s = semestre)
            |> List.map (fun (_, _, prom) -> prom)
          in
          let total = float_of_int (List.length datos) in
          let aprobados = List.filter (fun p -> p >= 70.0) datos |> List.length |> float_of_int in
          let reprobados = total -. aprobados in
          let porcentaje_aprobados = if total = 0.0 then 0.0 else (aprobados /. total) *. 100.0 in
          let porcentaje_reprobados = if total = 0.0 then 0.0 else (reprobados /. total) *. 100.0 in
          let promedio = promedio_notas datos in
          (profe, semestre, promedio, porcentaje_aprobados, porcentaje_reprobados)
        )
;;

let rendimiento_por_anio_profesor json =
  json
  |> member "estudiante"
  |> member "cursos"
  |> to_list
  |> List.map (fun curso ->
      let profesor = curso |> member "profe" |> to_string in
      let anio = curso |> member "anio" |> to_int in
      curso
      |> member "estudiantes"
      |> to_list
      |> List.map (fun est ->
          let promedio = est |> member "notas" |> promedio_general in
          (profesor, anio, promedio)
        )
  )
  |> List.flatten
  |> fun registros ->
      registros
      |> List.map (fun (p, a, _) -> (p, a))
      |> List.sort_uniq compare
      |> List.map (fun (profe, anio) ->
          let datos =
            registros
            |> List.filter (fun (p, a, _) -> p = profe && a = anio)
            |> List.map (fun (_, _, prom) -> prom)
          in
          let total = float_of_int (List.length datos) in
          let aprobados = List.filter (fun p -> p >= 70.0) datos |> List.length |> float_of_int in
          let reprobados = total -. aprobados in
          let porcentaje_aprobados = if total = 0.0 then 0.0 else (aprobados /. total) *. 100.0 in
          let porcentaje_reprobados = if total = 0.0 then 0.0 else (reprobados /. total) *. 100.0 in
          let promedio = promedio_notas datos in
          (profe, anio, promedio, porcentaje_aprobados, porcentaje_reprobados)
        )
;;

let rendimiento_historico_profesor json =
  let por_anio = rendimiento_por_anio_profesor json in

  por_anio
  |> List.map (fun (profe, _, _, _, _) -> profe)
  |> List.sort_uniq String.compare
  |> List.map (fun profe ->
      let desgloce =
        por_anio
        |> List.filter (fun (p, _, _, _, _) -> p = profe)
        |> List.map (fun (_, anio, promedio, aprob, reprob) -> (anio, promedio, aprob, reprob))
      in
      let promedio_hist =
        desgloce |> List.map (fun (_, prom, _, _) -> prom) |> promedio_notas
      in
      (profe, promedio_hist, desgloce)
    )
;;

(* ------------------------------------------------------------------------------------------------------------------ *)
(* ------------------------------------------------------ MAIN ------------------------------------------------------ *)
(* ------------------------------------------------------------------------------------------------------------------ *)

let generar_salida_json json =
  let estudiante_json =
    `Assoc [
      ("por_tema", `List (
        rendimiento_por_tema_estudiante json
        |> List.map (fun (nombre, curso, resumen) ->
          `Assoc [
            ("nombre", `String nombre);
            ("curso", `String curso);
            ("temas", resultado_a_json resumen)
          ])
      ));
      ("por_curso", `List (
        rendimiento_por_curso_estudiante json
        |> List.map (fun (nombre, curso, resumen) ->
          `Assoc [
            ("nombre", `String nombre);
            ("curso", `String curso);
            ("resumen", resultado_a_json resumen)
          ])
      ));
      ("por_semestre", `List (
        rendimiento_por_semestre_estudiante json
        |> List.map (fun (nombre, semestre, promedio) ->
          `Assoc [
            ("nombre", `String nombre);
            ("semestre", `Int semestre);
            ("promedio", `Float promedio)
          ])
      ));
      ("por_anio", `List (
        rendimiento_por_anio_con_desgloce json
        |> List.map (fun (nombre, anio, promedio, semestres) ->
          `Assoc [
            ("nombre", `String nombre);
            ("anio", `Int anio);
            ("promedio", `Float promedio);
            ("semestres", `List (
              List.map (fun (sem, prom) ->
                `Assoc [("semestre", `Int sem); ("promedio", `Float prom)]
              ) semestres
            ))
          ])
      ));
      ("historico", `List (
        rendimiento_historico_estudiante (rendimiento_por_anio_con_desgloce json)
        |> List.map (fun (nombre, promedio_hist, desgloce) ->
          `Assoc [
            ("nombre", `String nombre);
            ("promedio_historico", `Float promedio_hist);
            ("anios", `List (
              List.map (fun (anio, prom) ->
                `Assoc [("anio", `Int anio); ("promedio", `Float prom)]
              ) desgloce
            ))
          ])
      ))
    ]
  in

  let profesor_json =
    `Assoc [
      ("por_tema", `List (
        rendimiento_por_tema_profesor json
        |> List.map (fun (profe, curso, resumen) ->
          `Assoc [
            ("profesor", `String profe);
            ("curso", `String curso);
            ("temas", resultado_a_json resumen)
          ])
      ));
      ("por_curso", `List (
        rendimiento_por_curso_profesor json
        |> List.map (fun (profe, curso, resumen) ->
          `Assoc [
            ("profesor", `String profe);
            ("curso", `String curso);
            ("resumen", resultado_a_json resumen)
          ])
      ));
      ("por_semestre", `List (
        rendimiento_por_semestre_profesor json
        |> List.map (fun (profe, semestre, prom, aprob, reprob) ->
          `Assoc [
            ("profesor", `String profe);
            ("semestre", `Int semestre);
            ("promedio", `Float prom);
            ("aprobados", `Float aprob);
            ("reprobados", `Float reprob)
          ])
      ));
      ("por_anio", `List (
        rendimiento_por_anio_profesor json
        |> List.map (fun (profe, anio, prom, aprob, reprob) ->
          `Assoc [
            ("profesor", `String profe);
            ("anio", `Int anio);
            ("promedio", `Float prom);
            ("aprobados", `Float aprob);
            ("reprobados", `Float reprob)
          ])
      ));
      ("historico", `List (
        rendimiento_historico_profesor json
        |> List.map (fun (profe, promedio_hist, desgloce) ->
          `Assoc [
            ("profesor", `String profe);
            ("promedio_historico", `Float promedio_hist);
            ("anios", `List (
              List.map (fun (anio, prom, aprob, reprob) ->
                `Assoc [
                  ("anio", `Int anio);
                  ("promedio", `Float prom);
                  ("aprobados", `Float aprob);
                  ("reprobados", `Float reprob)
                ]
              ) desgloce
            ))
          ])
      ))
    ]
  in

  let resultado_final = `Assoc [
    ("estudiante", estudiante_json);
    ("profesor", profesor_json)
  ] in

  Yojson.Basic.to_file "data/rendimiento.json" resultado_final
;;

let () =
  let json = Yojson.Basic.from_file "data/solicitud.json" in

  let temas = rendimiento_por_tema_estudiante json in
  print_endline "\nRendimiento por tema por estudiante:";
  List.iter (fun (nombre_est, nombre_curso, temas) ->
    Printf.printf "\nEstudiante: %s - Curso: %s\n" nombre_est nombre_curso;
    List.iter (fun (tema, prom) ->
      Printf.printf "  %s: %.2f\n" tema prom
    ) temas
  ) temas;  

  let cursos = rendimiento_por_curso_estudiante json in
  print_endline "\nRendimiento por curso por estudiante:";
  List.iter (fun (nombre_est, nombre_curso, resumen) ->
    Printf.printf "\nEstudiante: %s - Curso: %s\n" nombre_est nombre_curso;
    List.iter (fun (tipo, promedio) ->
      Printf.printf "  %s: %.2f\n" tipo promedio
    ) resumen
  ) cursos;

  let semestres = rendimiento_por_semestre_estudiante json in
  print_endline "\nRendimiento por semestre por estudiante:";
  List.iter (fun (nombre, semestre, promedio) ->
    Printf.printf "- Estudiante: %s - Semestre: %d - Promedio: %.2f\n"
      nombre semestre promedio
  ) semestres;

  let anual_desgloce = rendimiento_por_anio_con_desgloce json in
  print_endline "\nRendimiento por año (con desglose) por estudiante:";
  List.iter (fun (nombre, anio, promedio, semestres) ->
    Printf.printf "- Estudiante: %s - Año: %d - Promedio: %.2f\n" nombre anio promedio;
    List.iter (fun (sem, prom) ->
      Printf.printf "   - Estudiante: %s - Semestre: %d - Promedio: %.2f\n" nombre sem prom
    ) semestres
  ) anual_desgloce;

  let historico = rendimiento_historico_estudiante anual_desgloce in
  print_endline "\nRendimiento histórico por estudiante:";
  List.iter (fun (nombre, promedio_hist, desgloce) ->
    Printf.printf "- Estudiante: %s - Histórico: %.2f - Desgloce:\n" nombre promedio_hist;
    List.iter (fun (anio, prom) ->
      Printf.printf "   - Estudiante: %s - Año: %d - Promedio: %.2f\n"
        nombre anio prom
    ) desgloce
  ) historico;

  let tema_prof = rendimiento_por_tema_profesor json in
  print_endline "\nRendimiento por tema por profesor:";
  List.iter (fun (profe, curso, resumen) ->
    Printf.printf "\nProfesor: %s - Curso: %s\n" profe curso;
    List.iter (fun (tema, promedio) ->
      Printf.printf "  %s: %.2f\n" tema promedio
    ) resumen
  ) tema_prof;

  let curso_prof = rendimiento_por_curso_profesor json in
  print_endline "\nRendimiento por curso por profesor:";
  List.iter (fun (profe, curso, resumen) ->
    Printf.printf "\nProfesor: %s - Curso: %s\n" profe curso;
    List.iter (fun (tipo, promedio) ->
      Printf.printf "  %s: %.2f\n" tipo promedio
    ) resumen
  ) curso_prof;

  let semestre_prof = rendimiento_por_semestre_profesor json in
  print_endline "\nRendimiento por semestre por profesor:";
  List.iter (fun (profe, semestre, prom, aprob, reprob) ->
    Printf.printf "- Profesor: %s - Semestre: %d - Promedio: %.2f\n" profe semestre prom;
    Printf.printf "   Aprobados: %.2f%% - Reprobados: %.2f%%\n" aprob reprob
  ) semestre_prof;

  let anio_prof = rendimiento_por_anio_profesor json in
  print_endline "\nRendimiento por año por profesor:";
  List.iter (fun (profe, anio, prom, aprob, reprob) ->
    Printf.printf "- Profesor: %s - Año: %d - Promedio: %.2f\n" profe anio prom;
    Printf.printf "   Aprobados: %.2f%% - Reprobados: %.2f%%\n" aprob reprob
  ) anio_prof;

  let historico_prof = rendimiento_historico_profesor json in
  print_endline "\nRendimiento histórico por profesor:";
  List.iter (fun (profe, promedio, desgloce) ->
    Printf.printf "- Profesor: %s - Histórico: %.2f - Desgloce:\n" profe promedio;
    List.iter (fun (anio, prom, aprob, reprob) ->
      Printf.printf "   - Año: %d - Promedio: %.2f - Aprobados: %.2f%% - Reprobados: %.2f%%\n"
        anio prom aprob reprob
    ) desgloce
  ) historico_prof;

  generar_salida_json json;
  print_endline "\nResultados exportados en data/rendimiento.json";
;;
