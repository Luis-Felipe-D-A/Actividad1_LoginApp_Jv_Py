/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package Clases;

/**
 *
 * @author 
 */
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class Conector {
    
    
    private static final String URL = "jdbc:mysql://localhost:3306/tecnar_app_java";
    private static final String USER = "root";
    private static final String PASSWORD = "";
    
    private Connection conexion;

   
    public Connection conectar() {
        try {
            if (conexion == null || conexion.isClosed()) {
                conexion = DriverManager.getConnection(URL, USER, PASSWORD);
                System.out.println("✅ Conexión exitosa");
            }
        } catch (SQLException e) {
            System.out.println("❌ Error de conexión: " + e.getMessage());
        }
        return conexion;
    }

    
    public PreparedStatement prepararStatement(String sql) throws SQLException {
        Connection conn = conectar();
        if (conn == null) {
            throw new SQLException("No se pudo establecer la conexión a la BD");
        }
        return conn.prepareStatement(sql);
    }

    
    public ResultSet ejecutarConsulta(PreparedStatement ps) throws SQLException {
        return ps.executeQuery();
    }

    
    public int ejecutarUpdate(PreparedStatement ps) throws SQLException {
        return ps.executeUpdate();
    }

    
    public void desconectar() {
        try {
            if (conexion != null && !conexion.isClosed()) {
                conexion.close();
                System.out.println("🔒 Conexión cerrada");
            }
        } catch (SQLException e) {
            System.out.println("⚠️ Error al desconectarse: " + e.getMessage());
        }
    }
}
