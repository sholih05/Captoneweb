-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 11, 2024 at 01:33 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `si_sawi`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_users`
--

CREATE TABLE `tb_users` (
  `id` int(11) NOT NULL,
  `username` varchar(40) NOT NULL,
  `email` varchar(40) NOT NULL,
  `password` varchar(40) NOT NULL,
  `re_password` varchar(35) NOT NULL,
  `level` enum('Admin','User') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_users`
--

INSERT INTO `tb_users` (`id`, `username`, `email`, `password`, `re_password`, `level`) VALUES
(1, 'azmi', 'muhammadazmi@gmail.com', '12345678', '12345678', 'Admin'),
(2, 'hibat', 'seno@gmail.com', 'scrypt:32768:8:1$WnLcPVz8tcArjVjH$072b58', '010503', 'Admin'),
(3, 'riyan', 'riyan@gmail.com', 'scrypt:32768:8:1$aiXWzhlZEu18MGEe$ec49b4', '12345678', 'Admin'),
(4, 'aqila', 'aqila@gmail.com', 'scrypt:32768:8:1$cgIjsT5MZJ3VFNat$cbda63', '12345678', 'Admin'),
(5, 'nasqi', 'nasqi@gmail', '010503', '010503', 'Admin'),
(6, 'akmal', 'akmal@gmail.com', '1414', '1414', 'Admin'),
(7, 'fakhrul', 'fakhrul@gmail.com', '1234', '1234', 'Admin'),
(8, 'solih', 'solih@gmail.com', '1234', '1234', 'Admin'),
(9, 'admin', 'nursolih05@gmail.com', '12345', '12345', 'Admin'),
(10, 'ndaru', 'ndaru@gmail.com', '123', '123', 'Admin'),
(11, 'Kosong', 'ri@hotmail.com', '123', '123', 'Admin'),
(12, 'Bayi', '7777@hotmail.com', '666', '666', 'Admin'),
(13, 'zaka', 'zakartm@gmail.com', '12345', '12345', ''),
(14, 'hibatrasis', 'hibarrasis@gmail.com', '12345', '12345', 'User'),
(15, 'dada', 'dada@gmail.com', '12345', '12345', 'Admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_users`
--
ALTER TABLE `tb_users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_users`
--
ALTER TABLE `tb_users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
