-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 11, 2024 at 02:55 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.0.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `review 1`
--

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `result` int(11) NOT NULL,
  `date` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `history_detection`
--

CREATE TABLE `history_detection` (
  `id` int(11) NOT NULL,
  `tanggal` timestamp NOT NULL DEFAULT current_timestamp(),
  `username` varchar(255) NOT NULL,
  `prediction` varchar(255) NOT NULL,
  `confidence` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `history_detection`
--

INSERT INTO `history_detection` (`id`, `tanggal`, `username`, `prediction`, `confidence`) VALUES
(1, '2024-01-10 22:59:56', 'bayu', 'Ulat Tanah (Agrotis sp)', 1);

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

CREATE TABLE `review` (
  `id` int(11) NOT NULL,
  `review` varchar(100) NOT NULL,
  `score` int(11) NOT NULL,
  `date` datetime DEFAULT current_timestamp(),
  `user_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`id`, `review`, `score`, `date`, `user_id`) VALUES
(1, 'bagus', 3, '2024-01-11 05:46:10', NULL),
(2, 'bagus', 3, '2024-01-11 05:46:50', NULL),
(3, 'jelek', 1, '2024-01-11 05:47:06', NULL),
(4, 'aplikasinya sangat baik', 5, '2024-01-11 05:47:42', NULL),
(5, 'aplikasinya sangat keren', 5, '2024-01-11 05:47:59', NULL),
(6, 'aplikasinya sangat keren', 5, '2024-01-11 05:48:26', NULL),
(7, 'kontol', 1, '2024-01-11 05:51:10', NULL),
(8, 'kontol', 1, '2024-01-11 05:51:17', NULL),
(9, 'anjing', 1, '2024-01-11 05:51:26', NULL),
(10, 'anjing', 1, '2024-01-11 05:51:32', NULL),
(11, 'bagus', 3, '2024-01-11 06:04:28', NULL),
(12, 'bagus', 3, '2024-01-11 06:04:38', NULL),
(13, 'bagus', 3, '2024-01-11 06:04:44', NULL),
(14, 'sangat baik', 5, '2024-01-11 06:04:55', NULL),
(15, 'sangat baik', 5, '2024-01-11 06:05:01', NULL),
(16, 'sangat baik', 5, '2024-01-11 06:05:06', NULL),
(17, 'aplikasi sangat buruk', 1, '2024-01-11 06:12:39', NULL),
(18, 'aplikasi sangat buruk', 1, '2024-01-11 06:12:51', NULL),
(19, 'anjay', 3, '2024-01-11 06:24:50', NULL),
(20, 'keren sih', 3, '2024-01-11 06:24:59', NULL),
(21, 'sangat baik', 5, '2024-01-11 06:25:08', NULL),
(22, 'nggk bagus', 3, '2024-01-11 08:30:51', NULL),
(23, 'nggk bagus', 3, '2024-01-11 08:30:58', NULL),
(24, 'biasa saja', 3, '2024-01-11 08:31:06', NULL),
(25, 'biasa saja', 3, '2024-01-11 08:31:12', NULL),
(26, '', 3, '2024-01-11 08:36:53', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(256) NOT NULL,
  `history_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `history_detection`
--
ALTER TABLE `history_detection`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `review`
--
ALTER TABLE `review`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_user_history` (`history_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `history_detection`
--
ALTER TABLE `history_detection`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `review`
--
ALTER TABLE `review`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `history`
--
ALTER TABLE `history`
  ADD CONSTRAINT `history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `review`
--
ALTER TABLE `review`
  ADD CONSTRAINT `review_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`);

--
-- Constraints for table `user`
--
ALTER TABLE `user`
  ADD CONSTRAINT `fk_user_history` FOREIGN KEY (`history_id`) REFERENCES `history` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
