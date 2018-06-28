const express = require('express');
const professorRouter = express.Router();
const professorController = require('../controllers/ProfessorController');

// Get all professors
professorRouter.get('/', professorController.professorsList);

// Get professor by id
professorRouter.get('/:id', professorController.professorDetail);

module.exports = professorRouter;
