/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Clases;

/**
 *
 * @author 
 */

import javax.swing.table.DefaultTableModel;
import java.sql.*;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import javax.swing.JOptionPane;

public class Usuarios {

    private final Conector con;

    public Usuarios() {
        con = new Conector();
    }

   
    public void registrarUsuarios(String nombre, String apellido, String email, String username, String clave, String rol) {
        String sql = "INSERT INTO usuarios (nombre, apellido, email, username, clave, rol) VALUES (?, ?, ?, ?, ?, ?)";
       try(PreparedStatement ps = con.prepararStatement(sql)){
            ps.setString(1, nombre);
            ps.setString(2, apellido);
            ps.setString(3, email);
            ps.setString(4, username);
            ps.setString(5, clave);
            ps.setString(6, rol);

            ps.executeUpdate();
            JOptionPane.showMessageDialog(null, "✅ Usuario agregado con éxito");
        } catch (SQLException e) {
            JOptionPane.showMessageDialog(null, "❌ Error al insertar usuario: " + e.getMessage());
        }
    }

    
    public boolean validarUsuario(String username, String clave) {
        String sql = "SELECT * FROM usuarios WHERE username = ? AND clave = ?";
        try (PreparedStatement ps = con.prepararStatement(sql)) {
            ps.setString(1, username);
            ps.setString(2, clave);
            ResultSet rs = con.ejecutarConsulta(ps);
            if (rs.next()) {
                return true;
            }
        } catch (SQLException e) {
            System.out.println("❌ Error validando usuario: " + e.getMessage());
        } finally {
            con.desconectar();
        }
        return false;
    }

    
    public Usuario obtenerUsuarioPorUsername(String username) {
        String sql = "SELECT * FROM usuarios WHERE username = ?";
        try (PreparedStatement ps = con.prepararStatement(sql)) {
            ps.setString(1, username);
            ResultSet rs = con.ejecutarConsulta(ps);
            if (rs.next()) {
                return new Usuario(
                    rs.getString("nombre"),
                    rs.getString("apellido"),
                    rs.getString("email"),
                    rs.getString("username"),
                    rs.getString("clave"),
                    rs.getString("rol")
                );
            }
        } catch (SQLException e) {
            System.out.println("❌ Error obteniendo usuario: " + e.getMessage());
        } finally {
            con.desconectar();
        }
        return null;
    }



public DefaultTableModel listarUsuarios() {
    String[] columnas = {"Nombre", "Apellido", "Email", "Username", "Rol"};
    DefaultTableModel modelo = new DefaultTableModel(null, columnas);

    String sql = "SELECT nombre, apellido, email, username, rol FROM usuarios";

    try (PreparedStatement ps = con.prepararStatement(sql);
         ResultSet rs = con.ejecutarConsulta(ps)) {

        while (rs.next()) {
            Object[] fila = new Object[5];
            fila[0] = rs.getString("nombre");
            fila[1] = rs.getString("apellido");
            fila[2] = rs.getString("email");
            fila[3] = rs.getString("username");
            fila[4] = rs.getString("rol");
            modelo.addRow(fila);
        }

    } catch (SQLException e) {
        JOptionPane.showMessageDialog(null, "❌ Error listando usuarios: " + e.getMessage());
    } finally {
        con.desconectar();
    }

    return modelo;
}

public void eliminarUsuario(String username) {
    String sql = "DELETE FROM usuarios WHERE username=?";
    try (PreparedStatement ps = con.prepararStatement(sql)) {
        ps.setString(1, username);
        ps.executeUpdate();
        JOptionPane.showMessageDialog(null, "✅ Usuario eliminado");
    } catch (SQLException e) {
        JOptionPane.showMessageDialog(null, "❌ Error eliminando usuario: " + e.getMessage());
    }

}
public boolean actualizarUsuario(String nombre, String apellido, String email, String username, String clave, String rol) {
    String sql = "UPDATE usuarios SET (nombre, apellido, email, username, clave, rol) VALUES (?, ?, ?, ?, ?, ?) WHERE username=?"; 
    try (PreparedStatement ps = con.prepararStatement(sql)) {
        ps.setString(1, nombre);
        ps.setString(2, apellido);
        ps.setString(3, email);
        ps.setString(4, clave);
        ps.setString(5, rol);
        ps.setString(6, username);

        int filasActualizadas = ps.executeUpdate();
        if (filasActualizadas > 0) {
            JOptionPane.showMessageDialog(null, "✅ Usuario actualizado con éxito");
            return true;
        } else {
            JOptionPane.showMessageDialog(null, "❌ No se encontró el usuario para actualizar");
        }
    } catch (SQLException e) {
        JOptionPane.showMessageDialog(null, "❌ Error actualizando usuario: " + e.getMessage());
    }
    return false;
}
}