/**
 * Copyright (c) 2021 Jacob WF House.
 *
 * This file is licensed under a MIT license.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to
 * deal in the Software without restriction, including without limitation the
 * rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
 * sell copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

pipeline {
    agent { label 'amd64 && poetry' }
    stages{
        stage('Install Dependencies') {
            steps {
                script {
                    timestamps {
                        sh(script: 'git submodule update --init --recursive', label: 'Initialize Submodules')
                        sh(script: 'poetry install --no-dev', label: 'Install Project Dependencies')
                    }
                }
            }
        }
        stage('Build Document') {
            steps {
                script {
                    timestamps {
                        sh(script: 'poetry run python -m sudo_pour_me_a_drink -page-numbers -no-crop-marks', label: 'Build Static Site')
                        archiveArtifacts(artifacts: '**/cocktails.pdf', allowEmptyArchive: false)
                    }
                }
            }
        }
    }
}
