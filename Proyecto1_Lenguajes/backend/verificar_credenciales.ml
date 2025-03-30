(* verificar_credenciales.ml *)
open Yojson.Basic.Util

(* Función para leer un archivo JSON y devolver la lista de usuarios *)
let leer_usuarios archivo =
  try
    let json = Yojson.Basic.from_file archivo in
    json |> member "users" |> to_list
  with
  | Yojson.Json_error e ->
      Printf.printf "Error al leer el archivo JSON (%s): %s\n" archivo e;
      []
  | _ ->
      Printf.printf "Error inesperado al leer el archivo %s.\n" archivo;
      []

(* Verifica si alguna de las credenciales coincide con algún usuario *)
let verificar_login credenciales usuarios =
  List.exists (fun cred ->
      let email = cred |> member "email" |> to_string in
      let password = cred |> member "password" |> to_string in
      List.exists (fun usuario ->
          let uemail = usuario |> member "email" |> to_string in
          let upassword = usuario |> member "password" |> to_string in
          email = uemail && password = upassword
        ) usuarios
    ) credenciales

(* Obtiene el partner del primer usuario que coincida con las credenciales *)
let obtener_partner credenciales usuarios =
  let rec aux creds =
    match creds with
    | [] -> None
    | cred :: rest ->
        let email = cred |> member "email" |> to_string in
        let password = cred |> member "password" |> to_string in
        try
          let usuario =
            List.find (fun u ->
                let uemail = u |> member "email" |> to_string in
                let upassword = u |> member "password" |> to_string in
                email = uemail && password = upassword
              ) usuarios in
          Some (usuario |> member "partner" |> to_string)
        with Not_found -> aux rest
  in
  aux credenciales

(* Main *)
let () =
  let credenciales_file = "data/credenciales.json" in
  let usuarios_file = "data/usuarios.json" in

  let credenciales = leer_usuarios credenciales_file in
  let usuarios = leer_usuarios usuarios_file in

  if verificar_login credenciales usuarios then
    match obtener_partner credenciales usuarios with
    | Some partner ->
        (* Imprime la línea que usará Python para determinar el partner *)
        Printf.printf "Partner: %s\n" partner
    | None ->
        Printf.printf "No se encontró el partner para las credenciales.\n"
  else
    Printf.printf "Login fallido: credenciales incorrectas.\n"
