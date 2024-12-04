-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 04-12-2024 a las 19:08:14
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `puentesdb`
--

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS `puentesdb` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `puentesdb`;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `datos_de_lectura`
--

CREATE TABLE `datos_de_lectura` (
  `idDato` int(11) NOT NULL,
  `peso` float DEFAULT NULL,
  `iothing` varchar(50) NOT NULL,
  `fecha_hora` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `idGalga` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `galga`
--

CREATE TABLE `galga` (
  `idGalga` int(11) NOT NULL,
  `ubicacion` varchar(50) NOT NULL,
  `fecha_instalacion` date NOT NULL,
  `idPuente` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `puente`
--

CREATE TABLE `puente` (
  `idPuente` int(11) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `ubicacion` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `idUsuario` int(11) NOT NULL,
  `correo` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `rol` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `datos_de_lectura`
--
ALTER TABLE `datos_de_lectura`
  ADD PRIMARY KEY (`idDato`),
  ADD KEY `datos_de_lectura_galga` (`idGalga`);

--
-- Indices de la tabla `galga`
--
ALTER TABLE `galga`
  ADD PRIMARY KEY (`idGalga`),
  ADD KEY `galga_puente` (`idPuente`);

--
-- Indices de la tabla `puente`
--
ALTER TABLE `puente`
  ADD PRIMARY KEY (`idPuente`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`idUsuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `datos_de_lectura`
--
ALTER TABLE `datos_de_lectura`
  MODIFY `idDato` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `galga`
--
ALTER TABLE `galga`
  MODIFY `idGalga` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT de la tabla `puente`
--
ALTER TABLE `puente`
  MODIFY `idPuente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `idUsuario` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `datos_de_lectura`
--
ALTER TABLE `datos_de_lectura`
  ADD CONSTRAINT `datos_de_lectura_galga` FOREIGN KEY (`idGalga`) REFERENCES `galga` (`idGalga`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_idGalga` FOREIGN KEY (`idGalga`) REFERENCES `galga` (`idGalga`);

--
-- Filtros para la tabla `galga`
--
ALTER TABLE `galga`
  ADD CONSTRAINT `galga_puente` FOREIGN KEY (`idPuente`) REFERENCES `puente` (`idPuente`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
