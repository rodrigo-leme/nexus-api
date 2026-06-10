<%@ Language="VBScript" CodePage=65001 %>
<%
' =====================================================================
' Space Code LTDA - Recebe o formulario de contato e grava em JSON
' Arquivo: data\contatos.json  (array de objetos {nome, sobrenome, mensagem})
' =====================================================================
Option Explicit
Response.Charset = "utf-8"

Dim nome, sobrenome, mensagem
nome      = Trim(Request.Form("nome"))
sobrenome = Trim(Request.Form("sobrenome"))
mensagem  = Trim(Request.Form("mensagem"))

' Validacao obrigatoria no servidor
If nome = "" Or sobrenome = "" Or mensagem = "" Then
    Response.Status = "400 Bad Request"
    Response.Write "<h1>Erro: todos os campos s&atilde;o obrigat&oacute;rios.</h1>"
    Response.End
End If

Function JsonEscape(s)
    s = Replace(s, "\", "\\")
    s = Replace(s, """", "\""")
    s = Replace(s, vbCrLf, "\n")
    s = Replace(s, vbLf, "\n")
    s = Replace(s, vbTab, "\t")
    JsonEscape = s
End Function

Dim fso, caminho, conteudo, novoItem, stream
Set fso = Server.CreateObject("Scripting.FileSystemObject")
caminho = Server.MapPath("data/contatos.json")

' Le o conteudo atual (UTF-8)
Set stream = Server.CreateObject("ADODB.Stream")
stream.Type = 2
stream.Charset = "utf-8"
If fso.FileExists(caminho) Then
    stream.Open
    stream.LoadFromFile caminho
    conteudo = stream.ReadText
    stream.Close
Else
    conteudo = "[]"
End If
If Len(conteudo) > 0 And AscW(Left(conteudo, 1)) = 65279 Then conteudo = Mid(conteudo, 2)  ' remove BOM
conteudo = Replace(Replace(Replace(conteudo, vbCr, ""), vbLf, ""), vbTab, "")
conteudo = Trim(conteudo)
If conteudo = "" Or conteudo = "[]" Then
    conteudo = "[]"
Else
    ' Relê preservando a formatação original
    stream.Open
    stream.LoadFromFile caminho
    conteudo = stream.ReadText
    stream.Close
    If Len(conteudo) > 0 And AscW(Left(conteudo, 1)) = 65279 Then conteudo = Mid(conteudo, 2)
    conteudo = Trim(conteudo)
End If

novoItem = "{""nome"": """ & JsonEscape(nome) & """, " & _
           """sobrenome"": """ & JsonEscape(sobrenome) & """, " & _
           """mensagem"": """ & JsonEscape(mensagem) & """}"

' Insere o novo objeto no array JSON existente
If conteudo = "[]" Then
    conteudo = "[" & vbCrLf & "  " & novoItem & vbCrLf & "]"
Else
    conteudo = Left(conteudo, InStrRev(conteudo, "]") - 1)
    conteudo = RTrim(conteudo)
    If Right(conteudo, 2) = vbCrLf Then conteudo = Left(conteudo, Len(conteudo) - 2)
    conteudo = conteudo & "," & vbCrLf & "  " & novoItem & vbCrLf & "]"
End If

' Grava de volta (UTF-8)
stream.Open
stream.WriteText conteudo
stream.SaveToFile caminho, 2
stream.Close
Set stream = Nothing
Set fso = Nothing
%>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Mensagem enviada — Space Code LTDA</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <section class="section" style="text-align:center; padding-top:120px;">
        <h2>Mensagem enviada com sucesso!</h2>
        <p>Obrigado, <strong><%= Server.HTMLEncode(nome) %> <%= Server.HTMLEncode(sobrenome) %></strong>.
           Sua mensagem foi registrada em nosso sistema.</p>
        <p><a href="index.html">&larr; Voltar ao site</a> · <a href="data/contatos.json">Ver contatos.json</a></p>
    </section>
</body>
</html>
